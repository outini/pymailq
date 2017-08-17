|PythonPIP|_ |PythonSupport|_ |License|_ |Codacy|_ |Coverage|_

pymailq - Simple Postfix queue management
=========================================

| **Contact:** Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
| **Sources:** https://github.com/outini/pymailq/
|
| A full content documentation, is online at http://outini.github.io/pymailq/.
|
| The pymailq module makes it easy to view and control Postfix mails queue. It
| provide several classes to store, view and interact with mail queue using
| Postfix command line tools. This module is provided for automation and
| monitoring developments.

Installation
------------

Install pymailq module from https://pypi.python.org::

    pip install pymailq

Install pymailq module from sources::

    python setup.py install

A SPEC file is also provided for RPM builds (currently tested only on Fedora),
thanks to Nils Ratusznik (https://github.com/ahpnils).

Requirements
------------

This module actually support the following Python versions:

  * *Python 2.7*
  * *Python 3*

A shell is provided for interactive administration. Based on Python *cmd*
module, *readline* is highly recommended to access shell's full features. A
full documentation on shell's usage is available at
http://outini.github.io/pymailq/pqshell.html

License
-------

"GNU GENERAL PUBLIC LICENSE" (Version 2) *(see LICENSE file)*


.. |PythonPIP| image:: https://badge.fury.io/py/pymailq.svg
.. _PythonPIP: https://pypi.python.org/pypi/pymailq/
.. |PythonSupport| image:: https://img.shields.io/badge/python-2.7,%203.4-blue.svg
.. _PythonSupport: https://github.com/outini/pymailq/
.. |License| image:: https://img.shields.io/badge/license-GPLv2-green.svg
.. _License: https://github.com/outini/pymailq/
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/8444a0f124fe463d86a91d80a2a52e7c
.. _Codacy: https://www.codacy.com/app/outini/pymailq
.. |Coverage| image:: https://api.codacy.com/project/badge/Coverage/8444a0f124fe463d86a91d80a2a52e7c
.. _Coverage: https://www.codacy.com/app/outini/pymailq
