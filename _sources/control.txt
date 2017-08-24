pyqueue.control -- Mails queue adminitrative operations
=======================================================

The :mod:`control` module define a basic python class to simplify
administrative operations against the mails queue. This module is mainly based
on the `postsuper`_ administrative tool functionnalities.

:class:`~control.QueueControl` Objects
--------------------------------------

    .. autoclass:: control.QueueControl()

    The :class:`~control.QueueControl` instance provides the following methods:

        .. automethod:: control.QueueControl._operate
        .. automethod:: control.QueueControl.delete_messages
        .. automethod:: control.QueueControl.hold_messages
        .. automethod:: control.QueueControl.release_messages
        .. automethod:: control.QueueControl.requeue_messages

.. External links for documentation
.. _postsuper: http://www.postfix.org/postsuper.1.html
