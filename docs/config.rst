.. _pymailq-configuration:

pymailq.CONFIG -- Configuration structure and usage
===================================================

PyMailq module takes an optional `.ini` configuration file.

Section: core
-------------

- ``postfix_spool``
    Path to postfix spool (defaults to `/var/spool/postfix`)

Section: commands
-----------------

- ``use_sudo`` (yes|no)
    Control the use of sudo to invoke commands (default: `yes`)
- ``list_queue``
    Command to list messages queue (default: `mailq`)
- ``cat_message``
    Command to cat message (default: `postcat -qv`)
- ``hold_message``
    Command to hold message (default: `postsuper -h`)
- ``release_message``
    Command to release message (default: `postsuper -H`)
- ``requeue_message``
    Command to requeue message (default: `postsuper -r`)
- ``delete_message``
    Command to delete message (default: `postsuper -d`)

Example
-------

**pymailq.ini**::

    [core]
    postfix_spool = /var/spool/postfix

    [commands]
    use_sudo = yes
    list_queue = mailq
    cat_message = postcat -qv
    hold_message = postsuper -h
    release_message = postsuper -H
    requeue_message = postsuper -r
    delete_message = postsuper -d
