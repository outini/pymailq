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


def run_cmd(command):
    """Run command in shell

    :param str command: Shell command
    :return: Shell response as :func:`str`
    """
    PQSHELL.onecmd(command)
    return answer()


def test_shell_init():
    """Test shell.PyMailqShell object"""
    assert hasattr(PQSHELL, "cmdloop_nointerrupt")
    assert PQSHELL.prompt == "PyMailq (sel:0)> "


def test_shell_exit():
    """Test shell.PyMailqShell object"""
    PQSHELL.cmdqueue = ['exit']
    PQSHELL.cmdloop_nointerrupt()
    assert "Exiting shell... Bye." in answer()


def test_empty_line():
    """Test empty line"""
    resp = run_cmd("")
    assert not len(resp)


def test_help():
    """Test 'help' command"""
    resp = run_cmd("help")
    assert "Documented commands" in resp


def test_help_help():
    """Test 'help help' command"""
    resp = run_cmd("help help")
    assert "Show available commands" in resp


def test_help_exit():
    """Test 'help exit' command"""
    resp = run_cmd("help exit")
    assert "Exit PyMailq shell" in resp


def test_help_show():
    """Test 'help show' command"""
    resp = run_cmd("help show")
    assert "Generic viewer utility" in resp


def test_help_store():
    """Test 'help store' command"""
    resp = run_cmd("help store")
    assert "Control of Postfix queue content storage" in resp


def test_help_select():
    """Test 'help select' command"""
    resp = run_cmd("help select")
    assert "Select mails from Postfix queue content" in resp


def test_help_inspect():
    """Test 'help inspect' command"""
    resp = run_cmd("help inspect")
    assert "Mail content inspector" in resp


def test_help_super():
    """Test 'help super' command"""
    resp = run_cmd("help super")
    assert "Call postsuper commands" in resp


def test_shell_store_status_unloaded():
    """Test 'store status' command with unloaded store"""
    resp = run_cmd("store status")
    assert "store is not loaded" in resp


def test_shell_store_load():
    """Test 'store load' command"""
    resp = run_cmd("store load")
    assert "mails loaded from queue" in resp


def test_shell_store_load_error():
    """Test 'store load' command"""
    resp = run_cmd("store load notfound.txt")
    assert "*** Error: unable to load store" in resp


def test_shell_store_status_loaded():
    """Test 'store status' command with loaded store"""
    resp = run_cmd("store status")
    assert "store loaded with " in resp


def test_shell_show():
    """Test 'show' command without arguments"""
    resp = run_cmd("show")
    assert "Generic viewer utility" in resp


def test_shell_show_invalid():
    """Test 'show invalid' command"""
    resp = run_cmd("show invalid")
    assert "*** Syntax error: show invalid" in resp
    resp = run_cmd("show selected limit invalid")
    assert "*** Syntax error: limit modifier needs a valid number" in resp


def test_shell_show_selected_limit():
    """Test 'show selected limit 2' command"""
    resp = run_cmd("show selected limit 2")
    assert "Preview of first 2" in resp
    assert len(resp.split('\n')) == 3
    resp = run_cmd("show selected limit 40")
    assert "Preview of first 40" not in resp
    assert len(resp.split('\n')) == 30


def test_shell_show_selected_sorted():
    """Test 'show selected sortby sender limit 2' command"""
    resp = run_cmd("show selected sortby sender asc limit 2")
    assert "Preview of first 2" in resp
    assert len(resp.split('\n')) == 3
    resp = run_cmd("show selected sortby sender desc limit 2")
    assert "Preview of first 2" in resp
    assert len(resp.split('\n')) == 3


def test_shell_show_selected_rankby():
    """Test 'show selected rankby' command"""
    resp = run_cmd("show selected rankby sender limit 2")
    assert "sender" in resp
    assert len(resp.split('\n')) == 5


def test_shell_show_filters_empty():
    """Test 'show filters' command without registered filters"""
    resp = run_cmd("show filters")
    assert "No filters applied on current selection" in resp


def test_shell_select():
    """Test 'select' command"""
    resp = run_cmd("select")
    assert "Select mails from Postfix queue content" in resp


def test_shell_select_sender():
    """Test 'select sender' command"""
    run_cmd("select sender sender-1")
    resp = run_cmd("show selected")
    assert "sender-1@" in resp
    assert len(resp.split('\n')) == 4
    run_cmd("select sender sender-1 exact")
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    resp = run_cmd("select sender sender-1 invalid")
    assert "invalid keyword: invalid" in resp


def test_shell_select_invalid():
    """Test 'select invalid' command"""
    resp = run_cmd("select invalid")
    assert "has no subcommand:" in resp


def test_shell_select_status():
    """Test 'select status' command"""
    resp = run_cmd("select status deferred")
    assert not len(resp)


def test_shell_select_size():
    """Test 'select size' command"""
    resp = run_cmd("select size XXX")
    assert "specified sizes must be valid numbers" in resp
    resp = run_cmd("select size 262 262")
    assert "multiple exact sizes specified" in resp
    resp = run_cmd("select size +262 +262")
    assert "multiple '-' sizes specified" in resp
    resp = run_cmd("select size -262 -262")
    assert "multiple '+' sizes specified" in resp
    run_cmd("store load")
    run_cmd("select reset")
    run_cmd("select size 262")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 8
    run_cmd("select reset")
    run_cmd("select size +260")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 30
    run_cmd("select reset")
    run_cmd("select size -262")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 10
    run_cmd("select reset")
    run_cmd("select size +261 -262")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 10


def test_shell_select_date():
    """Test 'select date' command"""
    run_cmd("store load")
    run_cmd("select reset")
    run_cmd("select date 2017-07-31")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 30
    run_cmd("select reset")
    run_cmd("select date 2017-07-30")
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    run_cmd("select reset")
    run_cmd("select date +2017-07-01")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 30
    run_cmd("select reset")
    run_cmd("select date +2017-08-31")
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    run_cmd("select reset")
    run_cmd("select date 2017-01-01..2017-08-31")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 30
    run_cmd("select reset")
    run_cmd("select date -2018-01-01")
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 30
    resp = run_cmd("select date XXXX-XX-XX")
    assert "'XXXX-XX-XX' does not match format '%Y-%m-%d'" in resp


def test_shell_show_filters():
    """Test 'show filters' command with registered filters"""
    run_cmd("select reset")
    run_cmd("select status deferred")
    expected = ("0: select status:\n"
                "    status: deferred")
    resp = run_cmd("show filters")
    assert expected == resp


def test_shell_select_replay():
    """Test 'select replay' command"""
    resp = run_cmd("select replay")
    assert "Selector resetted and filters replayed" in resp


def test_shell_select_rmfilter():
    """Test 'select rmfilter' command"""
    resp = run_cmd("select rmfilter 0")
    assert not len(resp)
    resp = run_cmd("select rmfilter 666")
    assert "invalid filter ID: 666" in resp


def test_shell_select_reset():
    """Test 'select reset' command"""
    resp = run_cmd("select reset")
    assert "Selector resetted with store content" in resp


def test_shell_super_delete():
    """Test 'select reset' command"""
    resp = run_cmd("super delete")
    assert "Deleted " in resp


def test_shell_super_hold():
    """Test 'select reset' command"""
    resp = run_cmd("super hold")
    assert "Put on hold " in resp


def test_shell_super_release():
    """Test 'select reset' command"""
    resp = run_cmd("super release")
    assert "Released " in resp


def test_shell_super_requeue():
    """Test 'super requeue' command"""
    resp = run_cmd("super requeue")
    assert "Requeued " in resp
