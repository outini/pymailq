|PythonPIP|_ |PythonSupport|_ |License|_ |Codacy|_ |Coverage|_ |RTFD|_ |Travis|_

pymailq - Simple Postfix queue management
=========================================

| **Contact:** Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
| **Sources:** https://github.com/outini/pymailq/
|
| A full content documentation, is online at https://pymailq.readthedocs.io/en/latest/
|
| The pymailq module makes it easy to view and control Postfix mails queue. It
| provide several classes to store, view and interact with mail queue using
| Postfix command line tools. This module is provided for automation and
| monitoring developments.
|
| This project also provides a shell-like to interact with Postfix mails queue.
| It provide simple means to view the queue content, filter mails on criterias
| like Sender or delivery errors and lead administrative operations.

Installation
------------

Install pymailq module from https://pypi.python.org::

    pip install pymailq

Install pymailq module from sources::

    python setup.py install

A SPEC file is also provided for RPM builds (currently tested only on Fedora),
thanks to Nils Ratusznik (https://github.com/ahpnils). Debian binary packages
are also available.

Requirements
------------

This module actually support the following Python versions:

*  *Python 2.7*
*  *Python 3+*

A shell is provided for interactive administration. Based on Python *cmd*
module, using Python compiled with *readline* support is highly recommended
to access shell's full features.

Using the shell
---------------

Mails queue summary::

    ~$ pqshell --summary

    ====================== Mail queue summary ========================
    Total mails in queue: 1773
    Total queue size: 40.2 MB

    Mails by accepted date:
        last 24h:          939
        1 to 4 days ago:   326
        older than 4 days: 173

    ----- Mails by status ----------    ----- Mails by size ----------
    Active      2                       Average size      23.239 KB
    Hold        896                     Maximum size    1305.029 KB
    Deferred    875                     Minimum size       0.517 KB

    ----- Unique senders -----------    ----- Unique recipients ------
    Senders     156                     Recipients          1003
    Domains     141                     Domains              240

    ----- Top senders ------------------------------------------------
    228    sender-3@domain-1.tld
    195    sender-1@domain-4.tld
    116    MAILER-DAEMON
    105    sender-2@domain-2.tld
    61     sender-7@domain-3.tld

    ----- Top sender domains -----------------------------------------
    228    domain-1.tld
    195    domain-4.tld
    105    domain-2.tld
    75     domain-0.tld
    61     domain-3.tld

    ----- Top recipients ---------------------------------------------
    29     user-1@domain-5.tld
    28     user-5@domain-9.tld
    23     user-2@domain-8.tld
    20     user-3@domain-6.tld
    20     user-4@domain-7.tld

    ----- Top recipient domains --------------------------------------
    697    domain-7.tld
    455    domain-5.tld
    37     domain-6.tld
    37     domain-9.tld
    34     domain-8.tld

Using the shell in interactive mode::

    ~$ pqshell
    Welcome to PyMailq shell.
    PyMailq (sel:0)> store load
    500 mails loaded from queue
    PyMailq (sel:500)> show selected limit 5
    2017-09-02 17:54:34 B04C91183774 [deferred] sender-6@test-domain.tld (425B)
    2017-09-02 17:54:34 B21D71183681 [deferred] sender-2@test-domain.tld (435B)
    2017-09-02 17:54:34 B422D11836AB [deferred] sender-7@test-domain.tld (2416B)
    2017-09-02 17:54:34 B21631183753 [deferred] sender-6@test-domain.tld (425B)
    2017-09-02 17:54:34 F2A7E1183789 [deferred] sender-2@test-domain.tld (2416B)
    ...Preview of first 5 (495 more)...
    PyMailq (sel:500)> show selected limit 5 long
    2017-09-02 17:54:34 B04C91183774 [deferred] sender-6@test-domain.tld (425B)
      Rcpt: user-3@test-domain.tld
       Err: Test error message
    2017-09-02 17:54:34 B21D71183681 [deferred] sender-2@test-domain.tld (435B)
      Rcpt: user-3@test-domain.tld
       Err: Test error message
    2017-09-02 17:54:34 B422D11836AB [deferred] sender-7@test-domain.tld (2416B)
      Rcpt: user-2@test-domain.tld
       Err: mail transport unavailable
    2017-09-02 17:54:34 B21631183753 [deferred] sender-6@test-domain.tld (425B)
      Rcpt: user-3@test-domain.tld
       Err: mail transport unavailable
    2017-09-02 17:54:34 F2A7E1183789 [deferred] sender-2@test-domain.tld (2416B)
      Rcpt: user-1@test-domain.tld
       Err: mail transport unavailable
    ...Preview of first 5 (495 more)...
    PyMailq (sel:500)> select error "Test error message"
    PyMailq (sel:16)> show selected rankby sender
    sender                                    count
    ================================================
    sender-2@test-domain.tld                  7
    sender-4@test-domain.tld                  3
    sender-6@test-domain.tld                  2
    sender-5@test-domain.tld                  1
    sender-8@test-domain.tld                  1
    sender-3@test-domain.tld                  1
    sender-1@test-domain.tld                  1
    PyMailq (sel:16)> select sender sender-2@test-domain.tld
    PyMailq (sel:7)> super hold
    postsuper: Placed on hold: 7 messages
    PyMailq (sel:7)> select reset
    Selector resetted with store content (500 mails)
    PyMailq (sel:500)> show selected rankby status
    status                                    count
    ================================================
    deferred                                  493
    hold                                      7
    PyMailq (sel:500)> exit
    Exiting shell... Bye.

Packaging
---------

Binary packages for some linux distribution are available. See the *packaging*
directory for more information.

License
-------

"GNU GENERAL PUBLIC LICENSE" (Version 2) *(see LICENSE file)*


.. |PythonPIP| image:: https://img.shields.io/pypi/v/pymailq.svg
.. _PythonPIP: https://pypi.python.org/pypi/pymailq/
.. |PythonSupport| image:: https://img.shields.io/badge/python-2.7,%203.4,%203.5,%203.6-blue.svg
.. _PythonSupport: https://github.com/outini/pymailq/
.. |License| image:: https://img.shields.io/badge/license-GPLv2-blue.svg
.. _License: https://github.com/outini/pymailq/
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/8444a0f124fe463d86a91d80a2a52e7c
.. _Codacy: https://www.codacy.com/app/outini/pymailq
.. |Coverage| image:: https://api.codacy.com/project/badge/Coverage/8444a0f124fe463d86a91d80a2a52e7c
.. _Coverage: https://www.codacy.com/app/outini/pymailq
.. |RTFD| image:: https://readthedocs.org/projects/pymailq/badge/?version=latest
.. _RTFD: http://pymailq.readthedocs.io/en/latest/?badge=latest
.. |Travis| image:: https://travis-ci.org/outini/pymailq.svg?branch=master
.. _Travis: https://travis-ci.org/outini/pymailq

