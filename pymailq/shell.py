#
#    Postfix queue control python tool (pymailq)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#    Copyright (C) 2014 Jocelyn Delalande <jdelalande@oasiswork.fr>
#
#    This file is part of pymailq
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import re
import cmd
from functools import partial
from datetime import datetime, timedelta
from subprocess import CalledProcessError
import shlex
import inspect
from pymailq import store, control, selector, utils

try:
    import readline
except ImportError as error:
    print("Python readline is not available, shell capabilities are limited.")


class StoreNotLoaded(Exception):
    def __str__(self):
        return 'The store is not loaded'


class PyMailqShell(cmd.Cmd):
    """PyMailq shell for interactive mode"""

    # Automatic building of supported methods and documentation
    commands_info = {
        'store': 'Control of Postfix queue content storage',
        'select': 'Select mails from Postfix queue content',
        'inspect': 'Mail content inspector',
        'super': 'Call postsuper commands'
        }

    # XXX: do_* methods are parsed before init and must be declared here
    do_store = None
    do_select = None
    do_super = None

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """Init method"""
        cmd.Cmd.__init__(self, completekey, stdin, stdout)

        # EOF action is registered here to hide it from user
        self.do_EOF = self.do_exit

        for command in self.commands_info:
            setattr(self, "help_%s" % (command,), partial(self._help_, command))
            setattr(self, "do_%s" % (command,), partial(self.__do, command))

        # show command is specific and cannot be build dynamically
        setattr(self, "help_show", partial(self._help_, "show"))

        self.pstore = store.PostqueueStore()
        self.selector = selector.MailSelector(self.pstore)
        self.qcontrol = control.QueueControl()

        # Formats for output
        self.format_parser = re.compile(r'\{[^{}]+\}')
        self.formats = {
                'brief': "{date} {qid} [{status}] {sender} ({size}B)",
                }

    def respond(self, answer):
        """Send reponse"""
        self.stdout.write(str(answer) + '\n')

    # Internal functions
    def emptyline(self):
        """Action on empty lines"""
        pass

    def help_help(self):
        """Help of command help"""
        self.respond("Show available commands")

    @staticmethod
    def do_exit(arg):
        """Action on exit"""
        return True

    def help_exit(self):
        """Help of command exit"""
        self.respond("Exit PyMailq shell (or use Ctrl-D)")

    def cmdloop_nointerrupt(self):
        """Specific cmdloop to handle KeyboardInterrupt"""
        can_exit = False
        # intro message is not in self.intro not to display it each time
        # cmdloop is restarted
        self.respond("Welcome to PyMailq shell.")
        while can_exit is not True:
            try:
                self.cmdloop()
                can_exit = True
            except KeyboardInterrupt:
                self.respond("^C")

    def postloop(self):
        cmd.Cmd.postloop(self)
        self.respond("\nExiting shell... Bye.")

    def _help_(self, command):
        docstr = self.commands_info.get(
                command, getattr(self, "do_%s" % (command,)).__doc__)
        self.respond(inspect.cleandoc(docstr))

        self.respond("Subcommands:")
        for method in dir(self):
            if method.startswith("_%s_" % (command,)):
                docstr = getattr(self, method).__doc__
                doclines = inspect.cleandoc(docstr).split('\n')
                self.respond("  %-10s %s" % (method[len(command)+2:],
                                             doclines.pop(0)))
                for line in doclines:
                    self.respond("  %-10s %s" % ("", line))

#
# PyMailq methods
#

    @property
    def prompt(self):
        """Dynamic prompt with usefull informations"""

        prompt = ['PyMailq']
        if self.selector is not None:
            prompt.append(' (sel:%d)' % (len(self.selector.mails)))
        prompt.append('> ')

        return "".join(prompt)

    def __do(self, cmd_category, str_arg):
        """Generic do_* method to call cmd categories"""

        args = shlex.split(str_arg)
        if not len(args):
            getattr(self, "help_%s" % (cmd_category,))()
            return None

        command = args.pop(0)
        method = "_%s_%s" % (cmd_category, command)
        try:
            lines = getattr(self, method)(*args)
            if lines is not None and len(lines):
                self.respond('\n'.join(lines))
        except AttributeError:
            self.respond("%s has no subcommand: %s" % (cmd_category, command))
        except (SyntaxError, TypeError) as exc:
            # Rewording Python TypeError message for cli display
            msg = str(exc)
            if "%s()" % (method,) in msg:
                msg = "%s command %s" % (cmd_category, msg[len(method)+3:])
            self.respond("*** Syntax error: " + msg)

    @staticmethod
    def get_modifiers(match, excludes=()):
        """Get modifiers from match

        :param str match: String to match in modifiers
        :param list excludes: Excluded modifiers
        :return: Matched modifiers as :func:`list`
        """
        modifiers = {
            'limit': ['<n>'],
            'rankby': ['<field>'],
            'sortby': ['<field> [asc|desc]']
        }
        if match in modifiers and match not in excludes:
            return modifiers[match]
        return [mod for mod in modifiers
                if mod not in excludes and mod.startswith(match)]

    def completenames(self, text, *ignored):
        """Complete known commands"""
        dotext = 'do_'+text
        suggests = [a[3:] for a in self.get_names() if a.startswith(dotext)]
        if len(suggests) == 1:
            # Only one suggest, return it with a space
            suggests[0] += " "
        return suggests

    def completedefault(self, text, line, *ignored):
        """Generic command completion method"""
        # we may consider the use of re.match for params in completion
        completion = {
            'show': {'__allow_mods__': True},
            'select': {
                'date': ['<datespec>'],
                'error': ['<error_msg>'],
                'rmfilter': ['<filterid>'],
                'sender': ['<sender> [exact]'],
                'size': ['<-n|n|+n> [-n]'],
                'status': ['<status>']
            }
        }

        args = shlex.split(line)
        command = args.pop(0)
        sub_command = ""
        if len(args):
            sub_command = args.pop(0)

        match = "_%s_" % (command,)
        suggests = [name[len(match):] for name in dir(self)
                    if name.startswith(match + sub_command)]

        # No suggests, return None
        if not len(suggests):
            return None

        # Return multiple suggests for sub-command
        if len(suggests) > 1:
            return suggests
        suggest = suggests.pop(0)

        exact_match = True if suggest == sub_command else False

        if suggest in completion.get(command, {}):
            if not exact_match:
                # Sub-command takes params, suffix it with a space
                return [suggest + " "]
            elif not len(args):
                # Return sub-command params
                return completion[command][sub_command]
        elif not exact_match:
            # Sub-command doesn't take params, return as is
            return [suggest]

        # Command allows modifiers
        if completion[command].get('__allow_mods__'):
            if len(args) or not len(text):
                match = args[-1] if len(args) else ""
                mods = self.get_modifiers(match, excludes=args[:-1])
                if not len(mods):
                    mods = self.get_modifiers("", excludes=args)
                mods[0] += " " if len(mods) == 1 else ""
                suggests = mods

        if not len(suggests):
            return None
        return suggests

    def _store_load(self, filename=None):
        """Load Postfix queue content"""
        try:
            self.pstore.load(filename=filename)
            # Automatic load of selector if it is empty and never used.
            if not len(self.selector.mails) and not len(self.selector.filters):
                self.selector.reset()
            return ["%d mails loaded from queue" % (len(self.pstore.mails))]
        except (OSError, IOError, CalledProcessError) as exc:
            return ["*** Error: unable to load store", "    %s" % (exc,)]

    def _store_status(self):
        """Show store status"""
        if self.pstore is None or self.pstore.loaded_at is None:
            return ["store is not loaded"]
        return ["store loaded with %d mails at %s" % (
                               len(self.pstore.mails), self.pstore.loaded_at)]

    def _select_reset(self):
        """Reset content of selector with store content"""
        self.selector.reset()
        return ["Selector resetted with store content (%s mails)" % (
                                                    len(self.selector.mails))]

    def _select_replay(self):
        """Reset content of selector with store content and replay filters"""
        self.selector.replay_filters()
        return ["Selector resetted and filters replayed"]

    def _select_rmfilter(self, filterid):
        """
        Remove filter previously applied
          Filters ids are used to specify filter to remove
          Usage: select rmfilter <filterid>
        """
        try:
            idx = int(filterid)
            self.selector.filters.pop(idx)
            self.selector.replay_filters()
        # TODO: except should be more accurate
        except:
            raise SyntaxError("invalid filter ID: %s" % filterid)

    def _select_status(self, status):
        """
        Select mails with specific postfix status
          Usage: select status <status>
        """
        self.selector.lookup_status(status=status)

    def _select_sender(self, sender, exact=False):
        """
        Select mails from sender
          Usage: select sender <sender> [exact]
        """
        if exact is not False:  # received from command line
            if exact != "exact":
                raise SyntaxError("invalid keyword: %s" % exact)
            exact = True
        self.selector.lookup_sender(sender=sender, exact=exact)

    def _select_size(self, sizeA, sizeB=None):
        """
        Select mails by size in Bytes
          - and + are supported, if not specified, search for exact size
          Size range is allowed by using - (lesser than) and + (greater than)
          Usage: select size <-n|n|+n> [-n]
        """
        smin = None
        smax = None
        exact = None
        try:
            for size in sizeA, sizeB:
                if size is None:
                    continue
                if exact is not None:
                    raise SyntaxError("exact size must be used alone")
                if size.startswith("-"):
                    if smax is not None:
                        raise SyntaxError("multiple max sizes specified")
                    smax = int(size[1:])
                elif size.startswith("+"):
                    if smin is not None:
                        raise SyntaxError("multiple min sizes specified")
                    smin = int(size[1:])
                else:
                    exact = int(size)
        except ValueError:
            raise SyntaxError("specified sizes must be valid numbers")

        if exact is not None:
            smin = exact
            smax = exact
        if smax is None:
            smax = 0
        if smin is None:
            smin = 0

        if smin > smax:
            raise SyntaxError("minimum size is greater than maximum size")

        self.selector.lookup_size(smin=smin, smax=smax)

    def _select_date(self, date_spec):
        """
        Select mails by date.
          Usage:
            select date <DATESPEC>
            Where <DATESPEC> can be
              YYYY-MM-DD (exact date)
              YYYY-MM-DD..YYYY-MM-DD (within a date range (included))
              +YYYY-MM-DD (after a date (included))
              -YYYY-MM-DD (before a date (included))
        """
        try:
            if ".." in date_spec:
                (str_start, str_stop) = date_spec.split("..", 1)
                start = datetime.strptime(str_start, "%Y-%m-%d")
                stop = datetime.strptime(str_stop, "%Y-%m-%d")
            elif date_spec.startswith("+"):
                start = datetime.strptime(date_spec[1:], "%Y-%m-%d")
                stop = datetime.now()
            elif date_spec.startswith("-"):
                start = datetime(1970, 1, 1)
                stop = datetime.strptime(date_spec[1:], "%Y-%m-%d")
            else:
                start = datetime.strptime(date_spec, "%Y-%m-%d")
                stop = start + timedelta(1)
            self.selector.lookup_date(start, stop)
        except ValueError as exc:
            raise SyntaxError(str(exc))

    def _select_error(self, error_msg):
        """
        Select mails by error message
        Specified error message can be partial
          Usage: select error <error_msg>
        """
        self.selector.lookup_error(str(error_msg))

    def viewer(function):
        """Result viewer decorator

        :param func function: Function to decorate
        """
        def wrapper(self, *args, **kwargs):
            args = list(args)  # conversion need for arguments cleaning
            limit = None
            overhead = 0
            try:
                if "limit" in args:
                    limit_idx = args.index('limit')
                    args.pop(limit_idx)  # pop option, next arg is value
                    limit = int(args.pop(limit_idx))
            except (IndexError, TypeError, ValueError):
                raise SyntaxError("limit modifier needs a valid number")

            output = "brief"
            for known in self.formats:
                if known in args:
                    output = args.pop(args.index(known))
                    break
            outformat = self.formats[output]

            elements = function(self, *args, **kwargs)

            total_elements = len(elements)
            if not total_elements:
                return ["No element to display"]

            # Check for headers and increase limit accordingly
            headers = 0
            if total_elements > 1 and "========" in str(elements[1]):
                headers = 2

            if limit is not None:
                if total_elements > (limit + headers):
                    overhead = total_elements - (limit + headers)
                else:
                    limit = total_elements
            else:
                limit = total_elements

            outformat_attrs = self.format_parser.findall(outformat)
            formatted = []
            for element in elements[:limit + headers]:
                if isinstance(element, store.Mail):
                    attrs = {}
                    for att in outformat_attrs:
                        attrs[att[1:-1]] = getattr(element, att[1:-1], "-")
                    formatted.append(outformat.format(**attrs))
                else:
                    formatted.append(element)

            if overhead > 0:
                msg = "...Preview of first %d (%d more)..." % (limit, overhead)
                formatted.append(msg)

            return formatted
        wrapper.__doc__ = function.__doc__
        return wrapper

    def do_show(self, str_arg):
        """
        Generic viewer utility
        Optionnal modifiers can be provided to alter output:
          limit <n>                     display the first n entries
          sortby <field> [asc|desc]     sort output by field asc or desc
          rankby <field>                Produce mails ranking by field
        Known fields:
          qid           Postqueue mail ID
          date          Mail date
          sender        Mail sender
          recipients    Mail recipients (list, no sort)
          size          Mail size
          errors        Postqueue deferred error messages (list, no sort)
        """
        args = shlex.split(str_arg)
        if not len(args):
            return self.help_show()

        sub_cmd = args.pop(0)
        try:
            lines = getattr(self, "_show_%s" % sub_cmd)(*args)
        except (TypeError, AttributeError):
            self.respond("*** Syntax error: show {0}".format(str_arg))
            return self.help_show()
        except SyntaxError as error:
            # Rewording Python TypeError message for cli display
            msg = str(error)
            if "%s()" % sub_cmd in msg:
                msg = "show command %s" % msg
            self.respond("*** Syntax error: " + msg)
            return self.help_show()

        self.respond("\n".join(lines))

    @viewer
    @utils.ranker
    @utils.sorter
    def _show_selected(self):
        """
        Show selected mails
          Usage: show selected [modifiers]
        """
        return self.selector.mails

    def _show_filters(self):
        """
        Show filters applied on current mails selection
          Usage: show filters
        """
        if not len(self.selector.filters):
            return ["No filters applied on current selection"]

        lines = []
        for idx, pqfilter in enumerate(self.selector.filters):
            name, _args, _kwargs = pqfilter
            # name should always be prefixed with lookup_
            lines.append('%d: select %s:' % (idx, name[7:]))
            for key in sorted(_kwargs):
                lines.append("    %s: %s" % (key, _kwargs[key]))
        return lines

    # Postsuper generic command
    def __do_super(self, operation, action_name):
        """Postsuper generic command"""
        if not self.pstore.loaded_at:
            raise StoreNotLoaded
        if not len(self.selector.mails):
            return ["No mail selected"]
        else:
            func = getattr(self.qcontrol, '%s_messages' % operation)
            try:
                resp = func(self.selector.mails)
            except RuntimeError as exc:
                return [str(exc)]

            # reloads the data
            self._store_load()
            self._select_replay()

        return [resp[-1]]

    def _super_delete(self):
        """Deletes the mails in current selection
          Usage: super delete
        """
        return self.__do_super('delete', 'Deleted')

    def _super_hold(self):
        """Put on hold the mails in current selection
          Usage: super hold
        """
        return self.__do_super('hold', 'Put on hold')

    def _super_release(self):
        """Releases from hold the mails in current selection
          Usage: super release
        """
        return self.__do_super('release', 'Released')

    def _super_requeue(self):
        """requeue the mails in current selection
          Usage: super requeue
        """
        return self.__do_super('requeue', 'Requeued')
