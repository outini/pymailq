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


PSTORE = store.PostqueueStore()
SELECTOR = selector.MailSelector(PSTORE)
QCONTROL = control.QueueControl()


@patch('sys.stderr', new_callable=Mock())
def test_debug_decorator(stderr):
    """Test pymailq.debug decorator"""
    @pymailq.debug
    def test():
        stderr.write("test\n")
    test()


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


def test_mail_parse():
    """Test Mail.parse method"""
    mail = PSTORE.mails[0]
    assert mail.parsed is False
    mail.parse()
    assert mail.parsed is True


def test_mail_dump():
    """Test Mail.dump method"""
    mail = PSTORE.mails[0]
    datas = mail.dump()
    assert "headers" in datas
    assert "postqueue" in datas


def test_selector_status():
    """Test MailSelector.lookup_status method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_status(["deferred"])
    assert type(mails) == list
    assert len(mails) == 5000


def test_selector_sender():
    """Test MailSelector.lookup_sender method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_sender("sender-1", exact=False)
    assert type(mails) == list
    assert len(mails) == 1000
    SELECTOR.reset()
    mails = SELECTOR.lookup_sender("sender-2@test-domain.tld")
    assert type(mails) == list
    assert len(mails) == 1000


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
    assert len(mails) == 5000
    SELECTOR.reset()
    mails = SELECTOR.lookup_date(stop=datetime.now())
    assert type(mails) == list
    assert len(mails) == 5000


def test_selector_size():
    """Test MailSelector.lookup_size method"""
    SELECTOR.reset()
    mails = SELECTOR.lookup_size()
    assert type(mails) == list
    assert len(mails) == 5000
    SELECTOR.reset()
    mails = SELECTOR.lookup_size(smax=500)
    assert type(mails) == list
    assert len(mails) == 2500


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


def test_control_as_user():
    """Test QueueControl.hold_messages"""
    with pytest.raises(RuntimeError) as exc:
        QCONTROL.hold_messages(PSTORE.mails[0:2])
    assert "postsuper: fatal: use of this command" in str(exc.value)


def test_control_nothing_done():
    """Test QueueControl on unexistent mail ID"""
    QCONTROL.use_sudo = True
    result = QCONTROL.hold_messages([store.Mail('XXXXXXXXX')])
    assert type(result) == list
    assert len(result) == 1
    assert not len(result[0])


def test_control_hold():
    """Test QueueControl.hold_messages"""
    QCONTROL.use_sudo = True
    result = QCONTROL.hold_messages(PSTORE.mails[0:2])
    assert type(result) == list
    assert "postsuper: Placed on hold: 2 messages" in result


def test_control_release():
    """Test QueueControl.release_messages"""
    QCONTROL.use_sudo = True
    result = QCONTROL.release_messages(PSTORE.mails[0:2])
    assert type(result) == list
    assert "postsuper: Released from hold: 2 messages" in result


def test_control_requeue():
    """Test QueueControl.requeue_messages"""
    QCONTROL.use_sudo = True
    result = QCONTROL.requeue_messages(PSTORE.mails[0:2])
    assert "postsuper: Requeued: 2 messages" in result


def test_control_delete():
    """Test QueueControl.delete_messages"""
    QCONTROL.use_sudo = True
    # We don't really delete messages to keep queue consistence for next tests
    result = QCONTROL.delete_messages([])
    assert type(result) == list
    assert not len(result[0])
