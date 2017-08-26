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
from datetime import datetime, timedelta
from pymailq import CONFIG, shell

try:
    from unittest.mock import create_autospec
except ImportError:
    from mock import create_autospec


MOCK_STDOUT = create_autospec(sys.stdout)
PQSHELL = shell.PyMailqShell(stdout=MOCK_STDOUT)
PQSHELL.qcontrol.use_sudo = True


def answer():
    """Get shell response

    :return: Output lines as :func:`str`
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


def test_shell_empty_line():
    """Test empty line"""
    resp = run_cmd("")
    assert not len(resp)


def test_shell_completion():
    """Test shell completion"""
    resp = PQSHELL.completenames("sho")
    assert ["show "] == resp
    resp = PQSHELL.completedefault("invalid", "invalid")
    assert resp is None
    resp = PQSHELL.completedefault("re", "select re")
    assert ["replay", "reset"] == sorted(resp)
    resp = PQSHELL.completedefault("sel", "show sel")
    assert ["selected"] == resp
    resp = PQSHELL.completedefault("", "show selected ")
    assert ["limit", "rankby", "sortby"] == sorted(resp)
    resp = PQSHELL.completedefault("", "show selected limit ")
    assert ["<n> "] == resp
    resp = PQSHELL.completedefault("", "show selected limit 5 ")
    assert ["rankby", "sortby"] == sorted(resp)
    resp = PQSHELL.completedefault("sen", "select sen")
    assert ["sender "] == resp
    resp = PQSHELL.completedefault("", "select sender ")
    assert ["<sender> [exact]"] == resp


def test_shell_help():
    """Test 'help' command"""
    resp = run_cmd("help")
    assert "Documented commands" in resp


def test_shell_help_help():
    """Test 'help help' command"""
    resp = run_cmd("help help")
    assert "Show available commands" in resp


def test_shell_help_exit():
    """Test 'help exit' command"""
    resp = run_cmd("help exit")
    assert "Exit PyMailq shell" in resp


def test_shell_help_show():
    """Test 'help show' command"""
    resp = run_cmd("help show")
    assert "Generic viewer utility" in resp


def test_shell_help_store():
    """Test 'help store' command"""
    resp = run_cmd("help store")
    assert "Control of Postfix queue content storage" in resp


def test_shell_help_select():
    """Test 'help select' command"""
    resp = run_cmd("help select")
    assert "Select mails from Postfix queue content" in resp


def test_shell_help_inspect():
    """Test 'help inspect' command"""
    resp = run_cmd("help inspect")
    assert "Mail content inspector" in resp


def test_shell_help_super():
    """Test 'help super' command"""
    resp = run_cmd("help super")
    assert "Call postsuper commands" in resp


def test_shell_store_status_unloaded():
    """Test 'store status' command with unloaded store"""
    resp = run_cmd("store status")
    assert "store is not loaded" in resp


def test_shell_store_load_error():
    """Test 'store load' command"""
    resp = run_cmd("store load notfound.txt")
    assert "*** Error: unable to load store" in resp


def test_shell_store_load():
    """Test 'store load' command"""
    resp = run_cmd("store load")
    assert "mails loaded from queue" in resp


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
    resp = run_cmd("show selected rankby")
    assert "*** Syntax error: rankby requires a field" in resp
    resp = run_cmd("show selected rankby invalid")
    assert "*** Syntax error: elements cannot be ranked by" in resp
    resp = run_cmd("show selected sortby")
    assert "*** Syntax error: sortby requires a field" in resp
    resp = run_cmd("show selected sortby invalid")
    assert "*** Syntax error: elements cannot be sorted by" in resp


def test_shell_show_selected_limit():
    """Test 'show selected limit 2' command"""
    resp = run_cmd("show selected limit 2")
    assert "Preview of first 2" in resp
    assert len(resp.split('\n')) == 3
    resp = run_cmd("show selected limit 10000")
    assert "Preview of first 10000" not in resp
    assert len(resp.split('\n')) == 500


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
    assert not len(run_cmd("select sender sender-1"))
    resp = run_cmd("show selected")
    assert "sender-1@" in resp
    assert len(resp.split('\n')) == 100
    assert not len(run_cmd("select sender sender-1 exact"))
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
    assert "exact size must be used alone" in resp
    resp = run_cmd("select size +262 +262")
    assert "multiple min sizes specified" in resp
    resp = run_cmd("select size -262 -262")
    assert "multiple max sizes specified" in resp
    resp = run_cmd("select size -263 +266")
    assert "minimum size is greater than maximum size" in resp
    assert 'mails loaded from queue' in run_cmd("store load")
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select size 1000"))
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select size +200"))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 500
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select size -1000"))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 250
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select size +200 -1000"))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 250


def test_shell_select_date():
    """Test 'select date' command"""
    five_days = timedelta(5)
    now = datetime.now().strftime('%Y-%m-%d')
    five_days_ago = (datetime.now() - five_days).strftime('%Y-%m-%d')
    in_five_days = (datetime.now() + five_days).strftime('%Y-%m-%d')
    assert 'mails loaded from queue' in run_cmd("store load")
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date %s" % now))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 500
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date %s" % five_days_ago))
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date +%s" % five_days_ago))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 500
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date +%s" % in_five_days))
    resp = run_cmd("show selected")
    assert "No element to display" in resp
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date %s..%s" % (five_days_ago,
                                                   in_five_days)))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 500
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select date -%s" % in_five_days))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 500
    resp = run_cmd("select date XXXX-XX-XX")
    assert "'XXXX-XX-XX' does not match format '%Y-%m-%d'" in resp


def test_shell_select_error():
    """Test 'select date' command"""
    assert 'mails loaded from queue' in run_cmd("store load")
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select error 'Test error message'"))
    resp = run_cmd("show selected")
    assert len(resp.split("\n")) == 16


def test_shell_show_filters():
    """Test 'show filters' command with registered filters"""
    assert 'Selector resetted with store content' in run_cmd("select reset")
    assert not len(run_cmd("select status deferred"))
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


def test_shell_super_hold():
    """Test 'select reset' command"""
    CONFIG['commands']['use_sudo'] = True
    resp = run_cmd("super hold")
    assert "postsuper: Placed on hold" in resp


def test_shell_super_release():
    """Test 'select reset' command"""
    CONFIG['commands']['use_sudo'] = True
    resp = run_cmd("super release")
    assert "postsuper: Released" in resp


def test_shell_super_requeue():
    """Test 'super requeue' command"""
    CONFIG['commands']['use_sudo'] = True
    resp = run_cmd("super requeue")
    assert "postsuper: Requeued" in resp


def test_shell_super_delete():
    """Test 'select reset' command"""
    CONFIG['commands']['use_sudo'] = True
    resp = run_cmd("super delete")
    assert "postsuper: Deleted" in resp
