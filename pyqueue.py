#! /usr/bin/env python2.7

#
#    Postfix queue control python tool (pyqueue)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
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

import sys
from datetime import datetime, timedelta
from pyqueue import store, control, selector, shell


#
# MAIN
#
# This is here for tests purpose, no administrative operations are made.
#
# The pyqueue.QueueControl object must be tested with specific code snippet:
# >>> import pyqueue
# >>> selector = MailSelector(PostqueueStore())
# >>> selector.lookup_sender("MAILER-DAEMON")
# >>> qcontrol = QueueControl()
# >>> print "\n".join(qcontrol.hold_messages(selector.mails))
# >>> print "\n".join(qcontrol.release_messages(selector.mails))
# >>> print "\n".join(qcontrol.requeue_messages(selector.mails))
#
if __name__ == "__main__":

    # Looking for "tests", shell is the default action
    if "tests" not in sys.argv:
        try:
            cli = shell.PyQueueShell()
            cli.cmdloop()
        except KeyboardInterrupt:
            print "\nSlapping the door is not so kind while exiting...."
        sys.exit(0)


    ################################################
    # if not shell, then pyqueue module validation

    def list_preview(datas, limit = 5):
        """Return at most "limit" elements of datas list"""
        if len(datas) > limit:
            overhead = len(datas) - limit
            print" ... Preview of first %s (%s more) ..." % (limit, overhead)
            return datas[:limit]
        else:
            return datas

    pstore = store.PostqueueStore()

    print "Loading postfix queue store"
    pstore.load()
    print "Loaded %d mails" % (len(pstore.mails))

    selector = selector.MailSelector(pstore)

    sender = "MAILER-DAEMON"
    print "Looking for mails from '%s'" % (sender)
    for mail in list_preview(selector.lookup_sender(sender = sender)):
        print "%s: [%s] %s: %s (%d errors)" % (mail.date, mail.qid, mail.sender,
                                               ", ".join(mail.recipients),
                                               len(mail.errors))

    errormsg = "Connection timed out"
    print "\nLooking for '%s' error message" % (errormsg)
    for mail in list_preview(selector.lookup_error(error_msg = errormsg)):
        print "%s: %s (%d errors)" % (mail.date, mail.sender, len(mail.errors))

    stop_date = datetime.now() - timedelta(days=5)
    print "\nLooking for mails older than %s" % (stop_date)
    for mail in list_preview(selector.lookup_date(stop = stop_date)):
        print "%s: *%s* %s (%d errors)" % (mail.date, mail.status,
                                           mail.sender, len(mail.errors))

    print "\nProceeding to selector reset (%s mails)" % (len(selector.mails))
    selector.reset()
    print "Selector resetted (%s mails)" % (len(selector.mails))

    status = "active"
    print "\nLooking for mails with postqueue status: %s" % (status)
    for mail in list_preview(selector.lookup_status(status = status)):
        print "%s: %s (%d recipients)" % (mail.date, mail.sender,
                                          len(mail.recipients))

    print "\nReplaying filters"
    selector.replay_filters()
    print "Found %s mails" % (len(selector.mails))

    print "\nLooking for fat mails (>100000B)"
    for mail in list_preview(selector.lookup_size(smin = 100000)):
        print "%s: [%s] %s (%dB)" % ( mail.date, mail.qid,
                                      mail.sender, mail.size )

    print "\nLooking for multiple recipients mails"
    mrcpt = [ mail for mail in pstore.mails if len(mail.recipients) > 1 ]
    for mail in list_preview(mrcpt):
        print "%s: [%s] %s (%dB): %d recipients" % ( mail.date, mail.qid,
                                                     mail.sender, mail.size,
                                                     len(mail.recipients))

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
