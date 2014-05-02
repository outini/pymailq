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

.. seealso::

    Python module:
        :mod:`pyqueue.shell` for interactive control of Postfix mails queue.

The :mod:`pyqueue` module defines the following attribute:

    .. autodata:: DEBUG

The :mod:`pyqueue` module defines the following decorators:

    .. autofunction:: debug(function)


PostqueueStore Objects
**********************

.. autoclass:: pyqueue.store.PostqueueStore()

The :class:`~store.PostqueueStore` instance provides the following methods:

    .. automethod:: pyqueue.store.PostqueueStore.load([method])
    .. automethod:: pyqueue.store.PostqueueStore._load_from_postqueue()
    .. automethod:: pyqueue.store.PostqueueStore._load_from_spool()
    .. automethod:: pyqueue.store.PostqueueStore._get_postqueue_output()
    .. automethod:: pyqueue.store.PostqueueStore._is_mail_id(mail_id)

QueueControl Objects
********************

.. autoclass:: pyqueue.control.QueueControl()

The :class:`~control.QueueControl` instance provides the following methods:

    .. automethod:: pyqueue.control.QueueControl._operate
    .. automethod:: pyqueue.control.QueueControl.delete_messages
    .. automethod:: pyqueue.control.QueueControl.hold_messages
    .. automethod:: pyqueue.control.QueueControl.release_messages
    .. automethod:: pyqueue.control.QueueControl.requeue_messages

MailSelector Objects
********************

.. autoclass:: pyqueue.selector.MailSelector(store)

The :class:`~selector.MailSelector` instance provides the following methods:

    .. automethod:: pyqueue.selector.MailSelector.filter_registration
    .. automethod:: pyqueue.selector.MailSelector.reset()
    .. automethod:: pyqueue.selector.MailSelector.replay_filters()
    .. automethod:: pyqueue.selector.MailSelector.lookup_status(status)
    .. automethod:: pyqueue.selector.MailSelector.lookup_sender(sender[, partial])
    .. automethod:: pyqueue.selector.MailSelector.lookup_error(error_msg)
    .. automethod:: pyqueue.selector.MailSelector.lookup_date([start[, stop]])
    .. automethod:: pyqueue.selector.MailSelector.lookup_size([smin[, smax]])

Mail Objects
************

.. autoclass:: pyqueue.store.Mail(mail_id[, size[, date[, sender]]])

The :class:`~store.Mail` instance provides the following methods:

    .. automethod:: pyqueue.store.Mail.parse()
    .. automethod:: pyqueue.store.Mail.dump()

MailHeaders Objects
*******************

.. autoclass:: pyqueue.store.MailHeaders()

.. External links for documentation
.. _postqueue: http://www.postfix.org/postqueue.1.html
.. _postcat: http://www.postfix.org/postcat.1.html
.. _postsuper: http://www.postfix.org/postsuper.1.html
