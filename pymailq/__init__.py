#
#    Postfix queue control python tool (pymailq)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of pymailq
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys
import shlex
from functools import wraps
from datetime import datetime

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

#: Boolean to control activation of the :func:`debug` decorator.
DEBUG = False

#: Current version of the package as :class:`str`.
VERSION = "0.7.0"

#: Module configuration as :class:`dict`.
CONFIG = {
    "core": {
        "postfix_spool": "/var/spool/postfix"
    },
    "commands": {
        "use_sudo": False,
        "list_queue": ["mailq"],
        "cat_message": ["postcat", "-qv"],
        "hold_message": ["postsuper", "-h"],
        "release_message": ["postsuper", "-H"],
        "requeue_message": ["postsuper", "-r"],
        "delete_message": ["postsuper", "-d"]
    }
}


def debug(function):
    """
    Decorator to print some call informations and timing debug on stderr.

    Function's name, passed args and kwargs are printed to stderr. Elapsed time
    is also print at the end of call. This decorator is based on the value of
    :data:`DEBUG`. If ``True``, the debug informations will be displayed.
    """
    @wraps(function)
    def run(*args, **kwargs):
        name = function.__name__
        if DEBUG is True:
            sys.stderr.write("[DEBUG] Running {0}\n".format(name))
            sys.stderr.write("[DEBUG]     args: {0}\n".format(args))
            sys.stderr.write("[DEBUG]   kwargs: {0}\n".format(kwargs))
            start = datetime.now()

        ret = function(*args, **kwargs)

        if DEBUG is True:
            stop = datetime.now()
            sys.stderr.write("[DEBUG] Exectime of {0}: {1} seconds\n".format(
                                        name, (stop - start).total_seconds()))

        return ret

    return run


def load_config(cfg_file):
    """
    Load module configuration from .ini file

    Information from this file are directly used to override values stored in
    :attr:`pymailq.CONFIG`.

    Commands from configuration file are treated using :func:`shlex.split` to
    properly transform command string to list of arguments.

    :param str cfg_file: Configuration file

    .. seealso::

        :ref:`pymailq-configuration`
    """
    global CONFIG

    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)

    if "core" in cfg.sections():
        if cfg.has_option("core", "postfix_spool"):
            CONFIG["core"]["postfix_spool"] = cfg.get("core", "postfix_spool")

    if "commands" in cfg.sections():
        for key in cfg.options("commands"):
            if key == "use_sudo":
                if cfg.get("commands", key) == "yes":
                    CONFIG["commands"]["use_sudo"] = True
            else:
                command = shlex.split(cfg.get("commands", key))
                CONFIG["commands"][key] = command
