:mod:`pyqueue` --- Simple Postfix queue management
==================================================

.. toctree::
   :maxdepth: 2

.. module:: pyqueue
   :synopsis: Simple Postfix queue management.
.. moduleauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
.. sectionauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>

The :mod:`pyqueue` module makes it easy to view and control Postfix mails
queue. It provide several classes to store, view and interact with mail queue
using Postfix command line tools. This module is provided for automation and
monitoring.

.. seealso:: :mod:`pyqueueshell` for interactive control of Postfix mails queue.

The :mod:`pyqueue` module defines the following attribute:

    .. autodata:: DEBUG

The :mod:`pyqueue` module defines the following decorators:

    .. autofunction:: debug(function)


PostqueueStore Objects
**********************

.. autoclass:: pyqueue.PostqueueStore()

The :class:`~pyqueue.PostqueueStore` instance provides the following methods:

    .. automethod:: PostqueueStore.load([method])
    .. automethod:: PostqueueStore._load_from_postqueue()
    .. automethod:: PostqueueStore._load_from_spool()
    .. automethod:: PostqueueStore._get_postqueue_output()
    .. automethod:: PostqueueStore._is_mail_id(mail_id)

QueueControl Objects
********************

.. autoclass:: pyqueue.QueueControl()

The :class:`~pyqueue.QueueControl` instance provides the following methods:

    .. automethod:: QueueControl._operate
    .. automethod:: QueueControl.delete_messages
    .. automethod:: QueueControl.hold_messages
    .. automethod:: QueueControl.release_messages
    .. automethod:: QueueControl.requeue_messages

MailSelector Objects
********************

.. autoclass:: pyqueue.MailSelector(store)

The :class:`~pyqueue.MailSelector` instance provides the following methods:

    .. automethod:: MailSelector.filter_registration
    .. automethod:: MailSelector.reset()
    .. automethod:: MailSelector.replay_filters()
    .. automethod:: MailSelector.lookup_status(status)
    .. automethod:: MailSelector.lookup_sender(sender[, partial])
    .. automethod:: MailSelector.lookup_error(error_msg)
    .. automethod:: MailSelector.lookup_date([start[, stop]])
    .. automethod:: MailSelector.lookup_size([smin[, smax]])

Mail Objects
************

.. autoclass:: pyqueue.Mail(mail_id[, size[, date[, sender]]])

The :class:`~pyqueue.Mail` instance provides the following methods:

    .. automethod:: Mail.parse()
    .. automethod:: Mail.dump()

MailHeaders Objects
*******************

.. autoclass:: pyqueue.MailHeaders()

.. External links for documentation
.. _postqueue: http://www.postfix.org/postqueue.1.html
.. _postcat: http://www.postfix.org/postcat.1.html
.. _postsuper: http://www.postfix.org/postsuper.1.html
