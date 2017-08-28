pymailq.selector -- Mails queue filtering
=========================================

The :mod:`selector` module mainly provide a selector class to interact with
structures from the :mod:`store` module.

:class:`~selector.MailSelector` Objects
---------------------------------------

    .. autoclass:: selector.MailSelector(store)

    The :class:`~selector.MailSelector` instance provides the following methods:

        .. automethod:: selector.MailSelector.filter_registration
        .. automethod:: selector.MailSelector.reset()
        .. automethod:: selector.MailSelector.replay_filters()
        .. automethod:: selector.MailSelector.get_mails_by_qids(qids)
        .. automethod:: selector.MailSelector.lookup_qids(qids)
        .. automethod:: selector.MailSelector.lookup_status(status)
        .. automethod:: selector.MailSelector.lookup_sender(sender[, partial])
        .. automethod:: selector.MailSelector.lookup_error(error_msg)
        .. automethod:: selector.MailSelector.lookup_date([start[, stop]])
        .. automethod:: selector.MailSelector.lookup_size([smin[, smax]])
