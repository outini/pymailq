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

        PyQueue (sel:0)> store status
        store is not loaded
        PyQueue (sel:0)> store load
        590 mails loaded from queue
        PyQueue (sel:590)> store status
        store loaded with 590 mails at 2014-05-05 13:43:22.592767

select
------

    Select mails from Postfix queue content

    **Subcommands**:

        **date**
            Select mails by date.

            Usage: ``select date X [Y]``

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

show
----

    Display the content of current mails selection or specific mail IDs.

    **Optionnal modifiers** can be provided to alter output:
        ``limit <n>``
            Display the first n entries.

        ``sortby <field> [asc|desc]``
            Sort output by field asc or desc.

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
 
