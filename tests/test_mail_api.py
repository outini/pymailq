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

from datetime import datetime
import pymailq
from pymailq import store, control, selector


pymailq.DEBUG = True

PSTORE = store.PostqueueStore()
SELECTOR = selector.MailSelector(PSTORE)
QCONTROL = control.QueueControl()


def test_store_load_from_postqueue():
    """Test PostqueueStore load from postqueue"""
    PSTORE.load()
    assert PSTORE.loaded_at is not None


def test_store_load_from_spool():
    """Test PostqueueStore load from spool"""
    PSTORE.load(method="spool")
    assert PSTORE.loaded_at is not None


def test_store_load_from_filename():
    """Test PostqueueStore load from file"""
    PSTORE.load(method="postqueue", filename="tests/samples/mailq.sample")
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
    mails = SELECTOR.lookup_status(["deferred"])
    assert type(mails) == list


def test_selector_sender():
    """Test MailSelector.lookup_sender method"""
    mails = SELECTOR.lookup_sender("sender-1", partial=True)
    assert type(mails) == list
    mails = SELECTOR.lookup_sender("sender-1@testsend_domain.tld")
    assert type(mails) == list


def test_selector_error():
    """Test MailSelector.lookup_error method"""
    mails = SELECTOR.lookup_error("mail transport unavailable")
    assert type(mails) == list


def test_selector_date():
    """Test MailSelector.lookup_date method"""
    mails = SELECTOR.lookup_date(start=datetime(1970, 1, 1))
    assert type(mails) == list
    mails = SELECTOR.lookup_date(stop=datetime.now())
    assert type(mails) == list


def test_selector_size():
    """Test MailSelector.lookup_size method"""
    mails = SELECTOR.lookup_size()
    assert type(mails) == list
    mails = SELECTOR.lookup_size(smax=500)
    assert type(mails) == list


def test_selector_replay_filters():
    """Test MailSelector.replay_filters method"""
    SELECTOR.replay_filters()
    return True


def test_control_delete():
    """Test QueueControl.delete_messages"""
    result = QCONTROL.delete_messages(PSTORE.mails[0:2])
    assert type(result) == list


def test_control_hold():
    """Test QueueControl.hold_messages"""
    result = QCONTROL.hold_messages(PSTORE.mails[0:2])
    assert type(result) == list


def test_control_release():
    """Test QueueControl.release_messages"""
    result = QCONTROL.release_messages(PSTORE.mails[0:2])
    assert type(result) == list


def test_control_requeue():
    """Test QueueControl.requeue_messages"""
    result = QCONTROL.requeue_messages(PSTORE.mails[0:2])
    assert type(result) == list
