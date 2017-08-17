pqshell -- A shell-like to interact with a Postfix mails queue
==============================================================

DESCRIPTION
***********

pqshell is a shell-like to interact with Postfix mails queue. It provide simple
means to view the queue content, filter mails on criterias like `Sender` or
`delivery errors` and lead administrative operations.

SYNOPSIS
********

    pqshell [options]

FEATURES
********

- Asynchronous interactions with Postfix mails queue.
- Mails filtering on various criterias.
- Administrative operations on mails queue
- History and autocomplete via readline, if installed.

OPTIONS
*******

No options supported.

SHELL COMMANDS
**************

An inside help is available with the help command. Each provided command takes
subcommands and command's help can be obtained while running it without
argument.

store
-----

    Control of Postfix queue content storage

    **Subcommands**:

        **status**
            Show store status.

        **load**
            Load Postfix queue content.

    **Example**::

        PyMailq (sel:0)> store status
        store is not loaded
        PyMailq (sel:0)> store load
        590 mails loaded from queue
        PyMailq (sel:590)> store status
        store loaded with 590 mails at 2014-05-05 13:43:22.592767

select
------

    Select mails from Postfix queue content. Filters are cumulatives and
    designed to simply implement advanced filtering with simple syntax. The
    default prompt will show how many mails are currently selected by all
    applied filters. Order of filters application is also important.

    **Subcommands**:

        **date**
            Select mails by date.

            Usage: ``select date <DATESPEC>``

            Where `<DATESPEC>` can be::

                YYYY-MM-DD (exact date)
                YYYY-MM-DD..YYYY-MM-DD (within a date range (included))
                +YYYY-MM-DD (after a date (included))
                -YYYY-MM-DD (before a date (included))

        **error**
            Select mails by error message. Specified error message can be
            partial and will be check against the whole error message.

            Usage: ``select error <error_msg>``

        **replay**
            Reset content of selector with store content and replay filters.

        **reset**
            Reset content of selector with store content, remove filters.

        **rmfilter**
            Remove filter previously applied. Filters ids are used to specify
            filter to remove.

            Usage: ``select rmfilter <filterid>``

        **sender**
            Select mails from sender.

            Usage: ``select sender <sender> [exact]``

        **size**
            Select mails by size in Bytes. Signs - and + are supported, if not
            specified, search for exact size. Size range is allowed by
            using ``-`` (lesser than) and ``+`` (greater than).

            Usage: ``select size <-n|n|+n> [-n]``

        **status**
            Select mails with specific postfix status.

            Usage: ``select status <status>``

    **Filtering Example**::

        PyMailq (sel:608)> select size -5000
        PyMailq (sel:437)> select sender MAILER-DAEMON
        PyMailq (sel:316)> select status active
        PyMailq (sel:0)>

    **Filters management**::

        PyMailq (sel:608)> select size -5000
        PyMailq (sel:437)> select sender MAILER-DAEMON
        PyMailq (sel:316)> show filters
        0: select size:
            smax: 5000
            smin: 0
        1: select sender:
            partial: True
            sender: MAILER-DAEMON
        PyMailq (sel:316)> select rmfilter 1
        PyMailq (sel:437)> select sender greedy-sender@domain.com
        PyMailq (sel:25)> select reset
        Selector resetted with store content (608 mails)
        PyMailq (sel:608)>

show
----

    Display the content of current mails selection or specific mail IDs.
    Modifiers have been implemented to allow quick output manipulation. These
    allow you to sort, limit or even output a ranking by specific field. By
    default, output is sorted by **date of acceptance** in queue.

    **Optionnal modifiers** can be provided to alter output:
        ``limit <n>``
            Display the first n entries.

        ``sortby <field> [asc|desc]``
            Sort output by field asc or desc. Default sorting is made
            descending.

        ``rankby <field>``
            Produce mails ranking by field.

    **Known fields:**

      * ``qid`` -- Postqueue mail ID.
      * ``date`` -- Mail date.
      * ``sender`` -- Mail sender.
      * ``recipients`` -- Mail recipients (list, no sort).
      * ``size`` -- Mail size.
      * ``errors`` -- Postqueue deferred error messages (list, no sort).

    **Subcommands:**

        **filters**
            Show filters applied on current mails selection.

            Usage: ``show filters``

        **selected**
            Show selected mails.

            Usage: ``show selected [modifiers]``

    **Example**::

        PyMailq (sel:608)> show selected limit 5
        2014-05-05 20:54:24 699C11831669 [active] jjj@dom1.com (14375B)
        2014-05-05 20:43:39 8D60C13C14C6 [deferred] bbb@dom9.com (39549B)
        2014-05-05 20:35:08 B0077198BC31 [deferred] rrr@dom2.com (4809B)
        2014-05-05 20:30:09 014E21AB4B78 [deferred] aaa@dom7.com (2450B)
        2014-05-05 20:25:04 CF1BE127A8D3 [deferred] xxx@dom2.com (4778B)
        ...Preview of first 5 (603 more)...
        PyMailq (sel:608)> show selected sortby sender limit 5 asc
        2014-05-02 11:36:16 40AA9149A9D7 [deferred] aaa@dom1.com (8262B)
        2014-05-01 05:30:23 5E0B2162BE63 [deferred] bbb@dom4.com (3052B)
        2014-05-02 05:30:20 653471AC5F76 [deferred] ccc@dom5.com (3052B)
        2014-05-02 09:49:01 A00D3159AEE [deferred] ddd@dom1.com (3837B)
        2014-05-05 18:18:59 98E9A790749 [deferred] ddd@dom2.com (1551B)
        ...Preview of first 5 (603 more)...
        PyMailq (sel:608)> show selected rankby sender limit 5
        sender                                    count
        ================================================
        jjj@dom8.com                              334
        xxx@dom4.com                              43
        nnn@dom1.com                              32
        ccc@dom3.com                              14
        sss@dom5.com                              13
        ...Preview of first 5 (64 more)...

