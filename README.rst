pymailq - Simple Postfix queue management
==========================================

* *Author:* Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
* *Contact:* Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
* *Sources:* https://github.com/outini/pymailq/

A full content documentation, is online at http://outini.github.io/pymailq/.

The pymailq module makes it easy to view and control Postfix mails queue. It
provide several classes to store, view and interact with mail queue using
Postfix command line tools. This module is provided for automation and
monitoring developments.

Installation
------------

Install pymailq module::

    python setup.py install

A SPEC file is also provided for RPM builds (currently tested only on Fedora), 
thanks to Nils Ratusznik (*https://github.com/ahpnils*).

Requirements
------------

This module actually support the following Python versions:

  * *Python 2.7*
  * *Python 3*

A shell is provided for interactive administration. Based on Python *cmd*
module, *readline* is highly recommended to access shell's full features. A
full documentation on shell's usage is available at
http://outini.github.io/pymailq/pqshell.html

**Used Python modules:**

  * **os** *(https://docs.python.org/2/library/os.html)*
  * **sys** *(https://docs.python.org/2/library/sys.html)*
  * **datetime** *(https://docs.python.org/2/library/datetime.html)*
  * **functools** *(https://docs.python.org/2/library/functools.html)*
  * **subprocess** *(https://docs.python.org/2/library/subprocess.html)*
  * **gc** *(https://docs.python.org/2/library/gc.html)*
  * **re** *(https://docs.python.org/2/library/re.html)*
  * **cmd** *(https://docs.python.org/2/library/cmd.html)*
  * **shlex** *(https://docs.python.org/2/library/shlex.html)*
  * **email** *(https://docs.python.org/2/library/email.html)*
  * **collections.Counter**
    *(https://docs.python.org/2/library/collections.html#collections.Counter)*

License
-------

"GNU GENERAL PUBLIC LICENSE" (Version 2) *(see LICENSE file)*
