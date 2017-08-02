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
from pymailq import shell
from unittest.mock import create_autospec, MagicMock


MOCK_STDOUT = create_autospec(sys.stdout)
PQSHELL = shell.PyMailqShell(stdout=MOCK_STDOUT)


def answer():
    """Get shell response

    :param int nr: Number of lines to return
    :return: Output lines
    """
    res = ""
    for call in MOCK_STDOUT.write.call_args_list:
        res += call[0][0]
    MOCK_STDOUT.reset_mock()
    return res.strip()


def test_shell_init():
    """Test shell.PyMailqShell object"""
    assert hasattr(PQSHELL, "cmdloop_nointerrupt")


def test_empty_line():
    """Test empty line"""
    PQSHELL.onecmd("")


def test_help():
    """Test 'help' command"""
    PQSHELL.onecmd("help")
    assert "Documented commands" in answer()


def test_help_help():
    """Test 'help help' command"""
    PQSHELL.onecmd("help help")
    assert "Show available commands" in answer()


def test_help_exit():
    """Test 'help exit' command"""
    PQSHELL.onecmd("help exit")
    assert "Exit PyMailq shell" in answer()


def test_help_show():
    """Test 'help show' command"""
    PQSHELL.onecmd("help show")
    assert "Generic viewer utility" in answer()


def test_help_store():
    """Test 'help store' command"""
    PQSHELL.onecmd("help store")
    assert "Control of Postfix queue content storage" in answer()


def test_help_select():
    """Test 'help select' command"""
    PQSHELL.onecmd("help select")
    assert "Select mails from Postfix queue content" in answer()


def test_help_inspect():
    """Test 'help inspect' command"""
    PQSHELL.onecmd("help inspect")
    assert "Mail content inspector" in answer()


def test_help_super():
    """Test 'help super' command"""
    PQSHELL.onecmd("help super")
    assert "Call postsuper commands" in answer()


def test_shell_store_status_unloaded():
    """Test 'store status' command with unloaded store"""
    PQSHELL.onecmd("store status")
    assert "store is not loaded" in answer()


def test_shell_store_load():
    """Test 'store load' command"""
    PQSHELL.onecmd("store load")
    assert "mails loaded from queue" in answer()


def test_shell_store_status_loaded():
    """Test 'store status' command with loaded store"""
    PQSHELL.onecmd("store status")
    assert "store loaded with " in answer()


def test_shell_show_selected_limit():
    """Test 'show selected limit 2' command"""
    PQSHELL.onecmd("show selected limit 2")
    reply = answer()
    assert "Preview of first 2" in reply
    assert len(reply.split('\n')) == 3


def test_shell_show_selected_rankby():
    """Test 'show selected rankby' command"""
    PQSHELL.onecmd("show selected rankby sender limit 2")
    reply = answer()
    assert "sender" in reply
    assert len(reply.split('\n')) == 5


def test_shell_select():
    """Test 'select' command"""
    PQSHELL.onecmd("select")
    assert "Select mails from Postfix queue content" in answer()


def test_shell_select_sender():
    """Test 'select sender' command"""
    PQSHELL.onecmd("select sender sender-1")
    PQSHELL.onecmd("show selected")
    reply = answer()
    assert "sender-1@" in reply
    assert len(reply.split('\n')) == 4


def test_shell_select_invalid():
    """Test 'select invalid' command"""
    PQSHELL.onecmd("select invalid")
    assert "has no subcommand:" in answer()


def test_shell_select_replay():
    """Test 'select replay' command"""
    PQSHELL.onecmd("select replay")
    assert "Selector resetted and filters replayed" in answer()


def test_shell_select_reset():
    """Test 'select reset' command"""
    PQSHELL.onecmd("select reset")
    assert "Selector resetted with store content" in answer()


def test_exit():
    """Test 'exit' command"""
    assert PQSHELL.onecmd("exit") is True
