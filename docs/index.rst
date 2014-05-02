:mod:`pyqueue` --- Simple Postfix queue management
==================================================

.. toctree::
   :maxdepth: 4

.. module:: pyqueue
   :synopsis: Simple Postfix queue management.
.. moduleauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
.. sectionauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>

The :mod:`pyqueue` package makes it easy to view and control Postfix mails
queue. It provide several classes to store, view and interact with mail queue
using Postfix command line tools. This module is provided for automation and
monitoring.

.. seealso::

    Python module:
        :mod:`pyqueue.shell` for interactive control of Postfix mails queue.

The :mod:`pyqueue` package defines the following attribute:

    .. autodata:: DEBUG

The :mod:`pyqueue` package defines the following decorators:

    .. autofunction:: debug(function)


:mod:`~pyqueue.store` Module
****************************

:class:`~store.PostqueueStore` Objects
--------------------------------------

    .. autoclass:: pyqueue.store.PostqueueStore()

    The :class:`~store.PostqueueStore` instance provides the following methods:

        .. automethod:: store.PostqueueStore.load([method])
        .. automethod:: store.PostqueueStore._load_from_postqueue()
        .. automethod:: store.PostqueueStore._load_from_spool()
        .. automethod:: store.PostqueueStore._get_postqueue_output()
        .. automethod:: store.PostqueueStore._is_mail_id(mail_id)

:class:`~store.Mail` Objects
----------------------------

    .. autoclass:: pyqueue.store.Mail(mail_id[, size[, date[, sender]]])

    The :class:`~store.Mail` instance provides the following methods:

        .. automethod:: store.Mail.parse()
        .. automethod:: store.Mail.dump()

:class:`~store.MailHeaders` Objects
-----------------------------------

    .. autoclass:: store.MailHeaders()


:mod:`control` Module
*********************

:class:`~control.QueueControl` Objects
--------------------------------------

    .. autoclass:: control.QueueControl()

    The :class:`~control.QueueControl` instance provides the following methods:

        .. automethod:: control.QueueControl._operate
        .. automethod:: control.QueueControl.delete_messages
        .. automethod:: control.QueueControl.hold_messages
        .. automethod:: control.QueueControl.release_messages
        .. automethod:: control.QueueControl.requeue_messages


:mod:`selector` Module
**********************

:class:`~selector.MailSelector` Objects
---------------------------------------

    .. autoclass:: selector.MailSelector(store)

    The :class:`~selector.MailSelector` instance provides the following methods:

        .. automethod:: selector.MailSelector.filter_registration
        .. automethod:: selector.MailSelector.reset()
        .. automethod:: selector.MailSelector.replay_filters()
        .. automethod:: selector.MailSelector.lookup_status(status)
        .. automethod:: selector.MailSelector.lookup_sender(sender[, partial])
        .. automethod:: selector.MailSelector.lookup_error(error_msg)
        .. automethod:: selector.MailSelector.lookup_date([start[, stop]])
        .. automethod:: selector.MailSelector.lookup_size([smin[, smax]])


.. External links for documentation
.. _postqueue: http://www.postfix.org/postqueue.1.html
.. _postcat: http://www.postfix.org/postcat.1.html
.. _postsuper: http://www.postfix.org/postsuper.1.html
