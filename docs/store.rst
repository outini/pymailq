pymailq.store -- Mails queue storage objects
============================================

The :mod:`store` module provide several objects to convert mails queue content
into python structures.

:class:`~store.PostqueueStore` Objects
--------------------------------------

    .. autoclass:: pymailq.store.PostqueueStore()

    The :class:`~store.PostqueueStore` instance provides the following methods:

        .. automethod:: store.PostqueueStore.load([method])
        .. automethod:: store.PostqueueStore._load_from_postqueue()
        .. automethod:: store.PostqueueStore._load_from_spool()
        .. automethod:: store.PostqueueStore._get_postqueue_output()
        .. automethod:: store.PostqueueStore._is_mail_id(mail_id)
        .. automethod:: store.PostqueueStore.summary()

:class:`~store.Mail` Objects
----------------------------

    .. autoclass:: pymailq.store.Mail(mail_id[, size[, date[, sender]]])

    The :class:`~store.Mail` instance provides the following methods:

        .. automethod:: store.Mail.parse()
        .. automethod:: store.Mail.dump()
        .. automethod:: store.Mail.show()

:class:`~store.MailHeaders` Objects
-----------------------------------

    .. autoclass:: store.MailHeaders()


.. External links for documentation
.. _postqueue: http://www.postfix.org/postqueue.1.html
.. _postcat: http://www.postfix.org/postcat.1.html
