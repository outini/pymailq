pyqueue.selector -- Mails queue filtering
=========================================

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
