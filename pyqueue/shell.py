#
#    Postfix queue control python tool (pyqueue)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#    Copyright (C) 2014 Jocelyn Delalande <jdelalande@oasiswork.fr>
#
#    This file is part of pyqueue
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
from subprocess import CalledProcessError
import shlex
from pyqueue import store, control, selector, utils


try:
    import readline
except ImportError as error:
    print("Python readline is not available, shell capabilities are limited.")

class StoreNotLoaded(Exception):
    def __str__(self):
        return 'The store is not loaded'

class PyQueueShell(cmd.Cmd, object):
    """PyQueue shell for interactive mode"""

    # Automatic building of supported methods and documentation
    commands_info = {
        'store': 'Control of Postfix queue content storage',
        'select': 'Select mails from Postfix queue content',
        'inspect': 'Mail content inspector',
        'super' : 'call postsuper commands'
        }

    # XXX: do_* methods are parsed before init and must be declared here
    do_store = None
    do_select = None
    do_show = None
    do_super = None

    def __init__(self):
        """Init method"""
        cmd.Cmd.__init__(self)

        # EOF action is registered here to hide it from user
        self.do_EOF = self.do_exit

        for command in self.commands_info:
            setattr(self, "help_%s" % (command), partial(self._help_, command))
            setattr(self, "do_%s" % (command), partial(self.__do, command))
            setattr(self, "complete_%s" % (command),
                          partial(self.__complete, command))
        # show command is specific and cannot be build dynamicly
        setattr(self, "help_show", partial(self._help_, "show"))
        setattr(self, "complete_show", partial(self.__complete, "show"))

        self.pstore = store.PostqueueStore()
        self.selector = selector.MailSelector(self.pstore)
        self.qcontrol = control.QueueControl()

        # Formats for output
        self.format_parser = re.compile(r'\{[^{}]+\}')
        self.formats = {
                'brief': "{date} {qid} [{status}] {sender} ({size}B)",
                }

    # Internal functions
    def emptyline(self):
        pass

    def help_help(self):
        print("Show available commands")

    def do_exit(self, arg):
        return True

    def help_exit(self):
        print("Exit PyQueue shell (or use Ctrl-D)")

    def cmdloop_nointerrupt(self):
        """Specific cmdloop to handle KeyboardInterrupt"""
        can_exit = False
        # intro message is not in self.intro not to display it each time
        # cmdloop is restarted
        print("Welcome to PyQueue shell.")
        while can_exit is not True:
            try:
                self.cmdloop()
                can_exit = True
            except (KeyboardInterrupt):
                print("^C")

    def postloop(self):
        cmd.Cmd.postloop(self)
        print("\nExiting shell... Bye.")

    # PyQueue methods help
    def __parse_docstring(self, docstring):
        doclines = [ line.strip() for line in docstring.split('\n')
                     if len(line.strip()) ]
        parsed_lines = []
        for line in doclines:
            indent = ""
            if line.startswith('..'):
                line = "  " + line[2:]  # indentation required
            parsed_lines.append("%s%s" % (indent, line))
        return parsed_lines

    def _help_(self, command):
        doc = self.commands_info.get(
                command, getattr(self, "do_%s" % (command)).__doc__)
        for line in self.__parse_docstring(doc):
            print(line)

        print("Subcommands:")
        for method in dir(self):
            if method.startswith("_%s_" % (command)):
                docstr = getattr(self, method).__doc__
                doclines = self.__parse_docstring(docstr)
                print("  %-10s %s" % (method[len(command)+2:],
                                      doclines.pop(0)))
                for line in doclines:
                    print("  %-10s %s" % ("", line))

#
# PyQueue methods
#

    @property
    def prompt(self):
        """Dynamic prompt with usefull informations"""

        prompt = ['PyQueue']
        if self.selector is not None:
            prompt.append(' (sel:%d)' % (len(self.selector.mails)))
        prompt.append('> ')

        return "".join(prompt)

    def __do(self, cmd_category, str_arg):
        """Generic do_* method to call cmd categories"""

        args = shlex.split(str_arg)
        if not len(args):
            getattr(self, "help_%s" % (cmd_category))()
            return None

        command = args.pop(0)
        method = "_%s_%s" % (cmd_category, command)
        print("args:", str(method))
        try:
            lines = getattr(self, method)(*args)
            if lines is not None and len(lines):
                print('\n'.join(lines))
        #except AttributeError as error:
        #    print(error)
        #    print("%s has no subcommand: %s" % (cmd_category, command))
        except (SyntaxError, TypeError) as error:
            # Rewording Python TypeError message for cli display
            msg = error.message
            if "%s()" % (method) in msg:
                msg = "%s command %s" %(cmd_category, msg[len(method)+3:])
            print("*** Syntax error:", msg)

    def __complete(self, cmd_category, text, line, begidx, endidx):
        """Generic command completion method"""
        # TODO: find a way to stop completion if no more arguments
        #       It will probably not be possible to build it in auto :/
        match = "_%s_" % (cmd_category)
        return [ sub[len(match):] for sub in dir(self)
                 if sub.startswith(match + text) ]

# Store commands
    def _store_load(self, filename = None):
        """Load Postfix queue content"""
        try:
            self.pstore.load(filename = filename)
            # Automatic load of selector if it is empty and never used.
            if not len(self.selector.mails) and not len(self.selector.filters):
                self.selector.reset()
            return ["%d mails loaded from queue" % (len(self.pstore.mails))]
        except (OSError, CalledProcessError) as error:
            return ["*** Error: unable to load store", "    {0}".format(error)]

    def _store_status(self):
        """Show store status"""
        if self.pstore is None or self.pstore.loaded_at is None:
            return ["store is not loaded"]
        return ["store loaded with %d mails at %s" % (
                               len(self.pstore.mails), self.pstore.loaded_at)]

# Selector commands
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
        ..Filters ids are used to specify filter to remove
        ..Usage: select rmfilter <filterid>
        """
        try:
            idx = int(filterid)
            self.selector.filters.pop(idx)
            self.selector.replay_filters()
        # TODO: except should be more accurate
        except:
            raise SyntaxError("invalid filter ID: %s" % (idx))

    def _select_status(self, status):
        """
        Select mails with specific postfix status
        ..Usage: select status <status>
        """
        self.selector.lookup_status(status = status)

    def _select_sender(self, sender, partial = True):
        """
        Select mails from sender
        ..Usage: select sender <sender> [exact]
        """
        if partial is not True:  # received from command line
            if partial != "exact":
                raise SyntaxError("invalid keyword: %s" % (partial))
            partial = False
        self.selector.lookup_sender(sender = sender, partial = partial)

    def _select_size(self, sizeA, sizeB = None):
        """
        Select mails by size in Bytes
        ..- and + are supported, if not specified, search for exact size
        ..Size range is allowed by using - (lesser than) and + (greater than)
        ..Usage: select size <-n|n|+n> [-n]
        """
        smin = None
        smax = None
        exact = None
        try:
            for size in sizeA, sizeB:
                if size is None:
                    continue
                if exact is not None and (smin, smax) != (None, None):
                    raise SyntaxError("exact size must be used alone")
                if size.startswith("-"):
                    if smax is not None:
                        raise SyntaxError("multiple '+' sizes specified")
                    smax = int(size[1:])
                elif size.startswith("+"):
                    if smin is not None:
                        raise SyntaxError("multiple '-' sizes specified")
                    smin = int(size[1:])
                else:
                    if exact is not None:
                        raise SyntaxError("multiple exact sizes specified")
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

        self.selector.lookup_size(smin = smin, smax = smax)

    def _select_date(self, dateA, dateB = None):
        """
        Select mails by date
        ..Usage: select date X [Y]
        """
        return ["Still not implemented"]

    def _select_error(self, error_msg):
        """
        Select mails by error message
        Specified error message can be partial
        ..Usage: select error <error_msg>
        """
        return ["Still not implemented"]


# Viewer commands and wrapper
    def viewer(function):
        """Result viewer decorator
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
            except (IndexError, TypeError):
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

            if limit is not None:
                if total_elements > limit:
                    overhead = total_elements - limit
                else:
                    limit = total_elements
            else:
                limit = total_elements

            outformat_attrs = self.format_parser.findall(outformat)
            formatted = []
            for element in elements[:limit]:
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
        ..limit <n>                     display the first n entries
        ..sortby <field> [asc|desc]     sort output by field asc or desc
        ..rankby <field>                Produce mails ranking by field
        Known fields:
        ..qid           Postqueue mail ID
        ..date          Mail date
        ..sender        Mail sender
        ..recipients    Mail recipients (list, no sort)
        ..size          Mail size
        ..errors        Postqueue deferred error messages (list, no sort)
        """
        args = shlex.split(str_arg)
        if not len(args):
            return self.help_show()

        subcmd = args.pop(0)
        try:
            lines = getattr(self, "_show_%s" % (subcmd))(*args)
        except (TypeError, AttributeError):
            print("*** Syntax error: show {0}".format(str_arg))
            return self.help_show()
        except (SyntaxError, TypeError) as error:
            # Rewording Python TypeError message for cli display
            msg = error.message
            if "%s()" % (method) in msg:
                msg = "%s command %s" %(cmd_category, msg[len(method)+3:])
            print("*** Syntax error:", msg)

        print("\n".join(lines))

    @viewer
    @utils.ranker
    @utils.sorter
    def _show_selected(self):
        """
        Show selected mails
        ..Usage: show selected [modifiers]
        """
        if self.selector.mails is None:
            return []

        return self.selector.mails

    def _show_filters(self):
        """
        Show filters applied on current mails selection
        ..Usage: show filters
        """
        if not len(self.selector.filters):
            return ["No filters applied on current selection"]

        lines = []
        for idx in range(len(self.selector.filters)):
            name, _args, _kwargs = self.selector.filters[idx]
            # name should always be prefixed with lookup_
            lines.append('%d: select %s:' % (idx, name[7:]))
            for key,value in list(_kwargs.items()):
                lines.append("    %s: %s" % (key, value))
        return lines

    # Postsuper generic command
    def _super__do(self, cmd, action_name):
        if not self.pstore.loaded_at:
            raise(StoreNotLoaded)
        if self.selector.mails is None:
            handled_c = 0
        else:
            f = getattr(self.qcontrol, '%s_messages' % cmd)
            f(self.selector.mails)
            handled_c = len(self.selector.mails)
            # reloads the data
            self._store_load()
            self._select_reset()

        return ['{} {} mails'.format(action_name, handled_c)]

    def _super_delete(self):
        """Deletes the mails in current selection
        ..Usage: super delete
        """
        return self._super__do('delete', 'Deleted')

    def _super_hold(self):
        """Put on hold the mails in current selection
        ..Usage: super hold
        """
        return self._super__do('hold', 'Put on hold')

    def _super_release(self):
        """Releases from hold the mails in current selection
        ..Usage: super release
        """
        return self._super__do('release', 'Released')

    def _super_requeue(self):
        """requeue the mails in current selection
        ..Usage: super requeue
        """
        return self._super__do('requeue', 'Requeued')
