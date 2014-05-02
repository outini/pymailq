pyqueue -- Simple Postfix queue management
==========================================

.. module:: pyqueue
   :synopsis: Simple Postfix queue management XXX.
.. moduleauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
.. sectionauthor:: Denis 'jawa' Pompilio <denis.pompilio@gmail.com>

The :mod:`pyqueue` package makes it easy to view and control Postfix mails
queue. It provide several classes to store, view and interact with mail queue
using Postfix command line tools. This module is provided for automation and
monitoring.

The :mod:`pyqueue` package defines the following attribute:

    .. autodata:: DEBUG

The :mod:`pyqueue` package defines the following decorators:

    .. autofunction:: debug(function)

The :mod:`pyqueue` package provides the following submodules:

.. toctree::
    :maxdepth: 1

    store
    selector
    control
    shell
