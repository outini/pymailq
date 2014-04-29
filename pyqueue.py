#! /usr/bin/env python2.7

"""
Simple Postfix postqueue manipulation tool
"""

__docformat__ = 'restructuredtext en'
__author__ = "Denis 'jawa' Pompilio"
__credits__ = "Denis 'jawa' Pompilio"
__license__ = "GPLv2"
__maintainer__ = "Denis 'jawa' Pompilio"
__email__ = "denis.pompilio@gmail.com"
__status__ = "Development"

import os
import sys
import subprocess
import email
from functools import wraps
from datetime import datetime, timedelta
import re
import gc

#: Boolean to control activation of the :func:`debug` decorator.
DEBUG = False

def debug(function):
    """
    Decorator to print some call informations and timing debug on stderr.
    
    Function's name, passed args and kwargs are printed to stderr. Elapsed time
    is also print at the end of call. This decorator is based on the value of
    :data:`DEBUG`. If ``True``, the debug informations will be displayed.
    """
    @wraps(function)
    def run(*args, **kwargs):
        name = function.func_name
        if DEBUG is True:
            print >> sys.stderr, "[DEBUG] Running {0}".format(name)
            print >> sys.stderr, "[DEBUG]     args: {0}".format(args)
            print >> sys.stderr, "[DEBUG]   kwargs: {0}".format(kwargs)
            start = datetime.now()

        ret = function(*args, **kwargs)

        if DEBUG is True:
            stop = datetime.now()
            print >> sys.stderr, "[DEBUG] Exectime of {0}: {1} seconds".format(
                    name, (stop - start).total_seconds())

        return ret

    return run

class MailHeaders(object):
    """
    Simple object to store mail headers.

    Object's attributes are dynamicly created while parent :class:`Mail`
    object's method :meth:`~Mail.parse` is called. Those attributes are
    retrieved with help of :func:`~email.message_from_string` method provided
    by the :mod:`email` module.

    Standard RFC *822-style* mail headers becomes attributes including but not
    limited to:

    - :mailheader:`Received`
    - :mailheader:`From`
    - :mailheader:`To`
    - :mailheader:`Cc`
    - :mailheader:`Bcc`
    - :mailheader:`Sender`
    - :mailheader:`Reply-To`
    - :mailheader:`Subject`

    Case is kept while creating attribute and access will be made with
    :attr:`Mail.From` or :attr:`Mail.Received` for example. All those
    attributes will return *list* of values.

    .. seealso::

        Python modules:
            :mod:`email` -- An email and MIME handling package

            :class:`email.message.Message` -- Representing an email message

        :rfc:`822` -- Standard for ARPA Internet Text Messages
    """

class Mail(object):
    """
    Simple object to manipulate email messages.

    This class provides the necessary methods to load and inspect mails
    content. This object functionnalities are mainly based on :mod:`email`
    module's provided class and methods. However,
    :class:`email.message.Message` instance's stored informations are
    extracted to extend :class:`Mail` instances attributes.

    Initialization of :class:`~pyqueue.Mail` instances are made the following
    way:

    :param str mail_id: Mail Postfix queue ID string
    :param int size: Mail size in Bytes
    :param datetime.datetime date: Mail :class:`datetime.datetime` object of
                                   reception time by Postfix
    :param str sender: Mail sender string as seen by Postfix

    The :class:`~pyqueue.Mail` class defines the following attributes:

        .. attribute:: qid

            Mail Postfix queue ID string, validated by
            :meth:`~PostqueueStore._is_mail_id` method.

        .. attribute:: size

            Mail size in bytes. :attr:`size` expected type is :func:`int`.

        .. attribute:: parsed

            :func:`bool` value to track if Mail content has been loaded from
            corresponding spool file.

        .. attribute:: parse_error
    
            Last encountered parse error message :func:`str`.

        .. attribute:: date

            Mail :class:`datetime.datetime` object of reception time by Postfix.

        .. attribute:: status
    
            Mail Postfix queue status :func:`str`. 

        .. attribute:: sender

            Mail sender :func:`str` as seen by Postfix.

        .. attribute:: recipients

            Recipients :func:`list` as seen by Postfix.

        .. attribute:: errors

            Mail deliver errors :func:`list` provided by Postfix.

        .. attribute:: head

            Mail headers :class:`~pyqueue.MailHeaders` structure.

        .. attribute:: postcat_cmd

            Postfix command and arguments :func:`list` for mails content
            parsing. Default command and arguments list is build at
            initialization with: ``["postcat", "-qv", self.qid]``
    """

    def __init__(self, mail_id, size = 0, date = None, sender = ""):
        """Init method"""
        self.parsed = False
        self.parse_error = ""
        self.qid = mail_id
        self.date = date
        self.status = ""
        self.size = int(size)
        self.sender = sender
        self.recipients = []
        self.errors = []
        self.head = MailHeaders()
        self.postcat_cmd = ["postcat", "-qv", self.qid]

        # Getting optionnal status from postqueue mail_id
        postqueue_status = { '*': "active", '!': "hold" }
        if mail_id[-1] in postqueue_status.keys():
            self.qid = mail_id[:-1]
        self.status = postqueue_status.get(mail_id[-1], "deferred")

    @debug
    def parse(self):
        """
        Parse message content.
        
        This method use Postfix mails content parsing command defined in
        :attr:`~Mail.postcat_cmd` attribute. This command is runned using
        :class:`subprocess.Popen` instance.

        Parsed headers become attributes and are retrieved with help of
        :func:`~email.message_from_string` function provided by the
        :mod:`email` module.

        .. seealso::
            Postfix manual:
                `postcat`_ -- Show Postfix queue file contents
 
        """
        child = subprocess.Popen(self.postcat_cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        (stdout,stderr) = child.communicate()

        raw_content = list()
        for line in stdout.split('\n'):
            if self.size == 0 and line[0:14] == "message_size: ":
                self.size = int(line[14:].strip().split()[0])
            elif self.date is None and line[0:13] == "create_time: ":
                self.date = datetime.strptime(line[13:].strip(),
                                                       "%a %b %d %H:%M:%S %Y")
            elif not len(self.sender) and line[0:8] == "sender: ":
                self.sender = line[8:].strip()
            elif line[0:14] == "regular_text: ":
                raw_content.append(line[14:])

        message = email.message_from_string('\n'.join(raw_content))

        for header in set(message.keys()):
            value = message.get_all(header)
            setattr(self.head, header, value)

        self.parsed = True

    @debug
    def dump(self):
        """
        Dump mail's gathered informations to a :class:`dict` object.

        Mails informations are splitted in two parts in dictionnary.
        ``postqueue`` key regroups every informations directly gathered from
        Postfix queue, while ``headers`` regroups :class:`MailHeaders`
        attributes converted from mail content with the :meth:`~Mail.parse`
        method.

        If mail has not been parsed with the :meth:`~Mail.parse` method,
        informations under the ``headers`` key will be empty.

        :return: Mail gathered informations
        :rtype: :class:`dict`
        """
        datas = {'postqueue': {},
                 'headers': {}}

        for attr in self.__dict__.keys():
            if attr[0] != "_" and attr != 'head':
                datas['postqueue'].update({ attr: getattr(self, attr) })

        for header in self.head.__dict__.keys():
            if header[0] != "_":
                datas['headers'].update({ header: getattr(self.head, header) })

        return datas

class PostqueueStore(object):
    """
    Postfix mails queue informations storage.

    The :class:`~pyqueue.PostqueueStore` provides methods to load Postfix
    queued mails informations into Python structures. Thoses structures are
    based on :class:`~pyqueue.Mail` and :class:`~pyqueue.MailHeaders` classes
    which can be processed by a :class:`~pyqueue.MailSelector` instance.

    The :class:`~pyqueue.PostqueueStore` class defines the following attributes:

        .. attribute:: mails

            Loaded :class:`Mail` objects :func:`list`.

        .. attribute:: loaded_at

            :class:`datetime.datetime` instance to store load date and time
            informations, useful for datas deprecation tracking. Updated on
            :meth:`~PostqueueStore.load` call with :meth:`datetime.datetime.now`
            method.

        .. attribute:: postqueue_cmd

            :class:`list` object to store Postfix command and arguments to view
            the mails queue content.
            Default is ``["/usr/sbin/postqueue", "-p"]``.

        .. attribute:: spool_path

            Postfix spool path string.
            Default is ``"/var/spool/postfix"``.

        .. attribute:: postqueue_mailstatus

            Postfix known queued mail status list.
            Default is ``['active', 'deferred', 'hold']``.

        .. attribute:: mail_id_re
    
            Python compiled regular expression object (:class:`re.RegexObject`)
            provided by :meth:`re.compile` method to match postfix IDs.
            Recognized IDs are hexadecimals, may be 10 to 12 chars length and
            followed with ``*`` or ``!``.
            Default used regular expression is: ``r"^[A-F0-9]{10,12}[*!]?$"``.

    .. seealso::

        Python modules:
            :mod:`datetime` -- Basic date and time types

            :mod:`re` -- Regular expression operations

        Postfix manual:
            `postqueue`_ -- Postfix queue control
    """
    postqueue_cmd = ["/usr/sbin/postqueue", "-p"]
    spool_path = "/var/spool/postfix"
    postqueue_mailstatus = ['active', 'deferred', 'hold']
    mail_id_re = re.compile(r"^[A-F0-9]{10,12}[*!]?$")

    def __init__(self):
        """Init method"""
        self.loaded_at = None
        self.mails = []

    @debug
    def _get_postqueue_output(self):
        """
        Get Postfix postqueue command output.

        This method used the postfix command defined in
        :attr:`~PostqueueStore.postqueue_cmd` attribute to view the mails queue
        content.

        Command defined in :attr:`~PostqueueStore.postqueue_cmd` attribute is
        runned using a :class:`subprocess.Popen` instance. Output headers
        (1 line) and footers (2 lines) are excluded from result.

        :return: Command's output lines without headers and footers.
        :rtype: :func:`list`

        .. seealso::

            Python module:
                :mod:`subprocess` -- Subprocess management
        """
        child = subprocess.Popen(self.postqueue_cmd,
                                 stdout=subprocess.PIPE)
        (stdout,stderr) = child.communicate()

        # return lines list without the headers and footers
        return [line.strip() for line in stdout.split('\n')][1:-2]

    def _is_mail_id(self, mail_id):
        """
        Check mail_id for a valid postfix queued mail ID.

        Validation is made using a :class:`re.RegexObject` stored in
        the :attr:`~PostqueueStore.mail_id_re` attribute of the
        :class:`PostqueueStore` instance.

        :param str mail_id: Mail Postfix queue ID string
        :return: True or false
        :rtype: :func:`bool`
        """

        if self.mail_id_re.match(mail_id) is None:
            return False
        return True

    @debug
    def _load_from_postqueue(self):  # TODO: documentation
        """
        Load content from postfix queue using postqueue command output.

        Output lines from :attr:`~PostqueueStore._get_postqueue_output` are
        parsed to build :class:`Mail` objects.

        Sample Postfix queue control tool output:
        ::
            C0004979687     4769 Tue Apr 29 06:35:05  sender@domain.com
            (error message from mx.remote1.org with parenthesis)
                                                     first.rcpt@remote1.org
            (error message from mx.remote2.org with parenthesis)
                                                     second.rcpt@remote2.org
                                                     third.rcpt@remote2.org
        """

        mail = None

        for line in self._get_postqueue_output():
            # Mails are blank line separated
            if not len(line):
                continue

            fields = line.split()
            if "(" == fields[0][0]:
                # Store error message without parenthesis: [1:-1]
                mail.errors.append(" ".join(fields)[1:-1])
            else:
                if self._is_mail_id(fields[0]):
                    # postfix does not precise year in mails timestamps
                    # we consider mails have been sent this year
                    # TODO: it may be improved
                    #       for Jan 1st usage with mails from prev year
                    current_year = datetime.now().year
                    date = datetime.strptime(
                            "%s %s" % (" ".join(fields[2:-1]), current_year),
                            "%a %b %d %H:%M:%S %Y")

                    mail = Mail(fields[0], size = fields[1],
                                           date = date,
                                           sender = fields[-1])
                    self.mails.append(mail)
                else:
                    #print "to: %s" % (fields[0])
                    mail.recipients.append(" ".join(fields))

    @debug
    def _load_from_spool(self):
        """
        Load content from postfix queue using files from spool.
        
        path defined in :attr:`~pyqueue.PostqueueStore.postqueue_cmd`
        attribute. Some :class:`~pyqueue.Mail` informations may be missing
        using the :meth:`~PostqueueStore._load_from_spool` method,
        including at least :attr:`~pyqueue.Mail.status` field.

        Loaded mails are stored as :class:`Mail` objects in
        :attr:`~PostqueueStore.mails` attribute.

        .. warning::
        
            Be aware that parsing mails on disk is slow and can lead to
            high load usage on system with large mails queue.
        """
        mail = None
        for status in self.postqueue_mailstatus:
            for path, dirs, files in os.walk("%s/%s" % (self.spool_path,
                                                        status)):
                for mail_id in files:
                    mail = Mail(mail_id)
                    mail.status = status

                    mail.parse()

                    self.mails.append(mail)

    @debug
    def load(self, method = "postqueue"):
        """
        Load content from postfix mails queue.
        
        Mails are loaded using postqueue command line tool or reading directly
        from spool. The optionnal argument, if present, is a method string and
        specifies the method used to gather mails informations. By default,
        method is set to ``"postqueue"`` and the standard Postfix queue
        control tool: `postqueue`_ is used.

        :param str method: Method used to load mails from Postfix queue

        Provided method :func:`str` name is directly used with :func:`getattr`
        to find a *self._load_from_<method>* method.
        """
        # releasing memory
        del self.mails
        gc.collect()

        self.mails = []
        getattr(self, "_load_from_{0}".format(method))()
        self.loaded_at = datetime.now()


class QueueControl(object):
    """
    Postfix queue control using postsuper command.

    The :class:`~pyqueue.QueueControl` instance defines the following
    attributes:

        .. attribute:: postsuper_cmd
 
            Postfix command and arguments list for mails queue administrative
            operations. Default is ``["postsuper"]``

        .. attribute:: known_operations

            Known Postfix administrative operations dictionnary to associate
            operations to command arguments. Known associations are:
            ::

                 delete: -d
                   hold: -h
                release: -H
                requeue: -r
    """

    postsuper_cmd = ["postsuper"]
    known_operations = {'delete': '-d',
                        'hold': '-h',
                        'release': '-H',
                        'requeue': '-r'}

    def _operate(self, operation, messages):
        """
        Generic method to lead operations messages from postfix mail queue.

        Operations can be one of Postfix known operations:
        :attr:`~QueueControl.known_operations`. Operation argument is directly
        converted and passed to the :attr:`~QueueControl.postsuper_cmd` command.
        """

        # Convert operation name to operation attribute. Raise KeyError.
        operation = self.known_operations[operation]

        # validate that object's attribute "qid" exist. Raise AttributeError.
        for msg in messages:
            getattr(msg, "qid")

        postsuper_cmd = self.postsuper_cmd + [operation, '-']
        child = subprocess.Popen(postsuper_cmd,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        for msg in messages:
            print >>child.stdin, msg.qid

        (stdout,stderr) = child.communicate()

        return [ line.strip() for line in stderr.split('\n') ]

    def delete_messages(self, messages):  # TODO: documentation
        """
        Delete several messages from postfix mail queue
        """
        return self._operate('delete', messages)

    def hold_messages(self, messages):  # TODO: documentation
        """
        Hold several messages from postfix mail queue
        """
        return self._operate('hold', messages)

    def release_messages(self, messages):  # TODO: documentation
        """
        Release several messages from postfix mail queue
        """
        return self._operate('release', messages)

    def requeue_messages(self, messages):  # TODO: documentation
        """
        Requeue several messages from postfix mail queue
        """
        return self._operate('requeue', messages)


class MailSelector(object):
    """
    Mail selector class to request mails from store matching criterias.

    The :class:`MailSelector` instance provides the following attributes:

    .. attribute:: mails

        Currently selected mails :func:`list`

    .. attribute:: store
    
        Linked :class:`~PostqueueStore` at the :class:`~MailSelector` instance
        initialization.

    .. attribute:: filters
    
        Applied filters :func:`list` on current selection. Filters list
        entries are tuple containing ``(function.__name__, args, kwargs)``
        for each applied filters. This list is filled by the
        :meth:`~MailSelector.filter_registration` decorator while calling
        filtering methods. It is possible to replay registered filter using
        :meth:`~MailSelector.replay_filters` method.
    """
    def __init__(self, store):
        """Init method"""
        self.mails = []
        self.store = store
        self.filters = []

        self.reset()

    def filter_registration(function):  # TODO: documentation
        """
        Decorator to register applied filter.
        """
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            filterinfo = (function.func_name, args, kwargs)
            self.filters.append(filterinfo)
            return function(self, *args, **kwargs)
        return wrapper

    def reset(self):  # TODO: documentation
        """
        Reset mail selector with initial store mails list.
        """
        del self.mails
        gc.collect()

        self.mails = [ mail for mail in self.store.mails ]
        self.filters = []

    def replay_filters(self):  # TODO: documentation
        """
        Reset selection with store content and replay registered filters.
        """
        del self.mails
        gc.collect()

        self.mails = [ mail for mail in self.store.mails ]
        filters = [ entry for entry in self.filters ]
        for filterinfo in filters:
            name, args, kwargs = filterinfo
            getattr(self, name)(*args, **kwargs)
        self.filters = filters

    @debug
    @filter_registration
    def lookup_status(self, status):  # TODO: documentation
        """
        Lookup mails with specified postqueue status.
        """
        if type(status) == str:
            status = [status]

        if not len(status):
            return self.mails

        self.mails = [ mail for mail in self.mails
                       if mail.status in status ]

        return self.mails


    @debug
    @filter_registration
    def lookup_sender(self, sender, partial = False):  # TODO: documentation
        """
        Lookup mails send from a specific sender.
        """
        if partial is False:
            self.mails = [ mail for mail in self.mails
                           if sender == mail.sender ]
        else:
            self.mails = [ mail for mail in self.mails
                           if sender in mail.sender ]

        return self.mails

    @debug
    @filter_registration
    def lookup_error(self, error_msg):  # TODO: documentation
        """
        Lookup mails with specific error message (message may be partial).
        """
        self.mails = [ mail for mail in self.mails
                       if True in [ True for err in mail.errors
                                    if error_msg in err ] ]
        return self.mails

    @debug
    @filter_registration
    def lookup_date(self, start = None, stop = None):   # TODO: documentation
        """
        Lookup mails send on specific date range.

        :param datetime.datetime start: Start date
        :param datetime.datetime start: Stop date
        :return: Matching :class:`Mail` objects from
                 :attr:`~PostqueueStore.mails`
        :rtype: :func:`list`
        """

        if start is None and stop is None:
            raise TypeError("Required arguments 'start' or 'stop' not found")

        if start is None:
            start = datetime(1970,1,1)
        if stop is None:
            stop = datetime.now()

        self.mails = [ mail for mail in self.mails
                       if mail.date >= start and mail.date <= stop ]

        return self.mails

    @debug
    @filter_registration
    def lookup_size(self, smin = 0, smax = 0):  # TODO: documentation
        """
        Lookup mails send with specific size.
        """
        if smin is 0 and smax is 0:
            return self.mails

        if smax > 0:
            self.mails = [ mail for mail in self.mails if mail.size <= smax ]
        self.mails = [ mail for mail in self.mails if mail.size >= smin ]

        return self.mails


# MAIN #
if __name__ == "__main__":

    def list_preview(datas, limit = 10):
        """Return at most "limit" elements of datas list"""
        if len(datas) > limit:
            overhead = len(datas) - limit
            print" ... Preview of first %s (%s more) ..." % (limit, overhead)
            return datas[:limit]
        else:
            return datas

    pstore = PostqueueStore()

    print "Loading postfix queue store"
    pstore.load()
    print "Loaded %d mails" % (len(pstore.mails))

    selector = MailSelector(pstore)

    sender = "MAILER-DAEMON"
    print "Looking for mails from '%s'" % (sender)
    for mail in list_preview(selector.lookup_sender(sender = sender,
                                                    partial=True)):
        print "%s: [%s] %s: %d errors" % (mail.date, mail.qid,
                                          mail.sender, len(mail.errors))
    print "Found %s mails" % (len(selector.mails))

    errormsg = "Connection timed out"
    print "\nLooking for '%s' error message" % (errormsg)
    for mail in list_preview(selector.lookup_error(error_msg = errormsg)):
        print "%s: %s (%d errors)" % (mail.date, mail.sender, len(mail.errors))
    print "Found %s mails" % (len(selector.mails))

    stop_date = datetime.strptime("2014-04-14", "%Y-%m-%d")
    print "\nLooking for mails older than %s" % (stop_date.isoformat())
    for mail in list_preview(selector.lookup_date(stop = stop_date)):
        print "%s: *%s* %s (%d errors)" % (mail.date, mail.status,
                                           mail.sender, len(mail.errors))
    print "Found %s mails" % (len(selector.mails))

    print "\nProceeding to selector reset (%s mails)" % (len(selector.mails))
    selector.reset()
    print "Selector resetted (%s mails)" % (len(selector.mails))

    status = "active"
    print "\nLooking for mails with postqueue status: %s" % (status)
    for mail in list_preview(selector.lookup_status(status = status)):
        print "%s: %s (%d recipients)" % (mail.date, mail.sender,
                                          len(mail.recipients))
    print "Found %s mails" % (len(selector.mails))

    print "\nReplaying filters"
    selector.replay_filters()
    print "Found %s mails" % (len(selector.mails))

    print "\nLooking for fat mails (>100000B)"
    for mail in list_preview(selector.lookup_size(smin = 100000)):
        print "%s: [%s] %s (%dB)" % ( mail.date, mail.qid,
                                      mail.sender, mail.size )
    print "Found %s mails" % (len(selector.mails))

    print "\nLooking for multiple recipients mails"
    mrcpt = [ mail for mail in pstore.mails if len(mail.recipients) > 1 ]
    for mail in list_preview(mrcpt):
        print "%s: [%s] %s (%dB)" % ( mail.date, mail.qid,
                                      mail.sender, mail.size )
    print "Found %s mails" % (len(mrcpt))

    target = pstore.mails[-1]
    print "\nDumping last mail from queue (%s)" % (target.qid)
    target.parse()
    datas = target.dump()
    print "Postqueue infos:"
    for k,v in datas['postqueue'].items():
        print "    %s: %s" % (k,v)
    print "Headers infos:"
    for k,v in datas['headers'].items():
        print "    %s: %s" % (k,v)

#    print "\nHolding selected mails from queue"
#    qcontrol = QueueControl()
#    print "\n".join(qcontrol.hold_messages(selector.mails))
