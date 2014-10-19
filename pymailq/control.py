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

import subprocess


class QueueControl(object):
    """
    Postfix queue control using postsuper command.

    The :class:`~control.QueueControl` instance defines the following
    attributes:

        .. attribute:: postsuper_cmd

            Postfix command and arguments :func:`list` for mails queue
            administrative operations. Default is ``["postsuper"]``

        .. attribute:: known_operations

            Known Postfix administrative operations :class:`dict` to associate
            operations to command arguments. Known associations are::

                 delete: -d
                   hold: -h
                release: -H
                requeue: -r

            .. warning::

                Default known associations are provided for the default mails
                queue administrative command `postsuper`_.

        .. seealso::

            Postfix manual:
                `postsuper`_ -- Postfix superintendent
    """

    postsuper_cmd = ["postsuper"]
    known_operations = {'delete': '-d',
                        'hold': '-h',
                        'release': '-H',
                        'requeue': '-r'}

    def _operate(self, operation, messages):
        """
        Generic method to lead operations messages from postfix mail queue.

        Operations can be one of Postfix known operations stored in
        :attr:`~QueueControl.known_operations` attribute. Operation
        argument is directly converted and passed to the
        :attr:`~QueueControl.postsuper_cmd` command.

        :param str operation: Known operation from
                              :attr:`~QueueControl.known_operations`.
        :param list messages: List of :class:`~store.Mail` objects targetted
                              for operation.
        :return: Command's *stderr* output lines
        :rtype: :func:`list`
        """
        # Convert operation name to operation attribute. Raise KeyError.
        operation = self.known_operations[operation]

        # validate that object's attribute "qid" exist. Raise AttributeError.
        for msg in messages:
            getattr(msg, "qid")

        postsuper_cmd = self.postsuper_cmd + [operation, '-']
        child = subprocess.Popen(postsuper_cmd,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        for msg in messages:
            child.stdin.write((msg.qid+'\n').encode())

        (stdout,stderr) = child.communicate()

        return [ line.strip() for line in stderr.decode().split('\n') ]

    def delete_messages(self, messages):
        """
        Delete several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``delete``
        """
        return self._operate('delete', messages)

    def hold_messages(self, messages):
        """
        Hold several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``hold``
        """
        return self._operate('hold', messages)

    def release_messages(self, messages):
        """
        Release several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``release``
        """
        return self._operate('release', messages)

    def requeue_messages(self, messages):
        """
        Requeue several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``requeue``
        """
        return self._operate('requeue', messages)
