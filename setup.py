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
import os
from distutils.core import setup

if __name__ == '__main__':
    release = open(os.path.join(os.path.dirname(__file__), "VERSION"), 'r').read().strip()
    setup(
        name = "pymailq",
        version = ".".join(release.split('.')),
        url = "https://github.com/outini/pymailq",
        author = "Denis Pompilio (jawa)",
        author_email = "denis.pompilio@gmail.com",
        maintainer = "Denis Pompilio (jawa)",
        maintainer_email = "denis.pompilio@gmail.com",
        description = "Postfix queue control python tool",
        long_description = open(os.path.join(os.path.dirname(__file__),
                                             'README.rst')).read(),
        license = "GPLv2",
        platforms = ['UNIX'],
        scripts = ['bin/pqshell'],
        packages = ['pymailq'],
        package_dir = {'pymailq': 'pymailq'},
        data_files = [('share/doc/pymailq',['README.rst', 'LICENSE']),
                      ('share/man/man1/', ['man/pqshell.1'])],
        keywords = ['postfix','shell','mailq','python','pqshell','postqueue'],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Operating System :: POSIX :: BSD',
            'Operating System :: POSIX :: Linux',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Programming Language :: Python',
            'Environment :: Console',
            'Topic :: Utilities',
            'Topic :: Communications :: Email',
            'Topic :: System :: Systems Administration',
            'Topic :: System :: Shells'
            ]
        )
