pymailq -- Simple Postfix queue management
==========================================

.. module:: pymailq
   :synopsis: Simple Postfix queue management XXX.
.. moduleauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
.. sectionauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>

The :mod:`pymailq` package makes it easy to view and control Postfix mails
queue. It provide several classes to store, view and interact with mail queue
using Postfix command line tools. This module is provided for automation and
monitoring.

The :mod:`pymailq` package defines the following attribute:

    .. autodata:: DEBUG

The :mod:`pymailq` package defines the following decorators:

    .. autofunction:: debug(function)

The :mod:`pymailq` package provides the following submodules:

.. toctree::
    :maxdepth: 1

    store
    selector
    control
    shell
    pqshell
