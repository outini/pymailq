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
import pytest
import pymailq
from datetime import datetime
from pymailq import store, control, selector

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


pymailq.CONFIG['commands']['use_sudo'] = True

PSTORE = store.PostqueueStore()
SELECTOR = selector.MailSelector(PSTORE)
QCONTROL = control.QueueControl()


@patch('sys.stderr', new_callable=Mock())
def test_debug_decorator(stderr):
    """Test pymailq.debug decorator"""
    pymailq.DEBUG = True

    @pymailq.debug
    def test():
        stderr.write("test\n")

    test()
    pymailq.DEBUG = False


def test_load_config():
    """Test pymailq.load_config method"""
    pymailq.CONFIG.update({"core": {}, "commands": {}})
    pymailq.load_config("tests/samples/pymailq.ini")
    assert 'postfix_spool' in pymailq.CONFIG['core']
    assert pymailq.CONFIG['commands']['use_sudo'] is True


def test_store_load_from_spool():
    """Test PostqueueStore load from spool"""
    PSTORE.load(method="spool")
    assert PSTORE.loaded_at is not None


def test_store_load_from_filename():
    """Test PostqueueStore load from file"""
    PSTORE.load(method="postqueue", filename="tests/samples/mailq.sample")
    assert PSTORE.loaded_at is not None


def test_store_load_from_postqueue():
    """Test PostqueueStore load from postqueue"""
    PSTORE.load()
    assert PSTORE.loaded_at is not None


def test_store_summary():
    """Test PostqueueStore.summary method"""
    summary = PSTORE.summary()
    assert 'top_senders' in summary
    assert 'top_recipients' in summary


def test_mail_parse_and_dump():
    """Test Mail.parse method"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    mail = store.Mail(PSTORE.mails[0].qid)
    assert mail.parsed is False
    mail.parse()
    assert mail.parsed is True
    datas = mail.dump()
    assert "headers" in datas
    assert "postqueue" in datas


def test_selector_get_mails_by_qids():
    """Test MailSelector.get_mails_by_qids method"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    SELECTOR.reset()
    qids = [mail.qid for mail in SELECTOR.mails[:2]]
    mails = SELECTOR.get_mails_by_qids(qids)
    assert len(mails) == 2
    assert qids[0] in mails[0].show()
    assert qids[1] in mails[1].show()


def test_selector_qids():
    """Test MailSelector.lookup_qids method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_qids([mail.qid for mail in PSTORE.mails[:2]])
    assert type(mails) == list
    assert len(mails) == 2


def test_selector_status():
    """Test MailSelector.lookup_status method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_status(["deferred"])
    assert type(mails) == list
    assert len(mails) == 500


def test_selector_sender():
    """Test MailSelector.lookup_sender method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_sender("sender-1", exact=False)
    assert type(mails) == list
    assert len(mails) == 100
    SELECTOR.reset()
    mails = SELECTOR.lookup_sender("sender-2@test-domain.tld")
    assert type(mails) == list
    assert len(mails) == 100


def test_selector_error():
    """Test MailSelector.lookup_error method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_error("Test error message")
    assert type(mails) == list
    assert len(mails) == 16


def test_selector_date():
    """Test MailSelector.lookup_date method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_date(start=datetime(1970, 1, 1))
    assert type(mails) == list
    assert len(mails) == 500
    SELECTOR.reset()
    mails = SELECTOR.lookup_date(stop=datetime.now())
    assert type(mails) == list
    assert len(mails) == 500


def test_selector_size():
    """Test MailSelector.lookup_size method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_size()
    assert type(mails) == list
    assert len(mails) == 500
    SELECTOR.reset()
    mails = SELECTOR.lookup_size(smax=1000)
    assert type(mails) == list
    assert len(mails) == 250
    SELECTOR.reset()
    mails = SELECTOR.lookup_size(smin=1000)
    assert type(mails) == list
    assert len(mails) == 250


def test_selector_replay_filters():
    """Test MailSelector.replay_filters method"""
    SELECTOR.replay_filters()
    return True


def test_selector_reset():
    """Test MailSelector.reset method"""
    assert SELECTOR.mails != PSTORE.mails
    SELECTOR.reset()
    assert not len(SELECTOR.filters)
    assert SELECTOR.mails == PSTORE.mails


def test_control_unknown_command():
    """Test QueueControl._operate with unknown command"""
    orig_command = pymailq.CONFIG['commands']['hold_message']
    pymailq.CONFIG['commands']['use_sudo'] = False
    pymailq.CONFIG['commands']['hold_message'] = ["invalid-cmd"]
    with pytest.raises(RuntimeError) as exc:
        QCONTROL.hold_messages([store.Mail('XXXXXXXXX')])
    assert "Unable to call" in str(exc.value)
    pymailq.CONFIG['commands']['hold_message'] = orig_command


def test_control_as_user():
    """Test QueueControl.hold_messages"""
    pymailq.CONFIG['commands']['use_sudo'] = False
    with pytest.raises(RuntimeError) as exc:
        QCONTROL.hold_messages([store.Mail('XXXXXXXXX')])
    assert "postsuper: fatal: use of this command" in str(exc.value)


def test_control_nothing_done():
    """Test QueueControl on unexistent mail ID"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    result = QCONTROL.hold_messages([store.Mail('XXXXXXXXX')])
    assert type(result) == list
    assert len(result) == 1
    assert not len(result[0])


def test_control_hold():
    """Test QueueControl.hold_messages"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    result = QCONTROL.hold_messages(PSTORE.mails[-2:])
    assert type(result) == list
    assert "postsuper: Placed on hold: 2 messages" in result


def test_control_release():
    """Test QueueControl.release_messages"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    result = QCONTROL.release_messages(PSTORE.mails[-2:])
    assert type(result) == list
    assert "postsuper: Released from hold: 2 messages" in result


def test_control_requeue():
    """Test QueueControl.requeue_messages"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    result = QCONTROL.requeue_messages(PSTORE.mails[-2:])
    assert "postsuper: Requeued: 2 messages" in result


def test_control_delete():
    """Test QueueControl.delete_messages"""
    pymailq.CONFIG['commands']['use_sudo'] = True
    # We don't really delete messages to keep queue consistence for next tests
    result = QCONTROL.delete_messages([])
    assert type(result) == list
    assert not len(result[0])
