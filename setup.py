#
#    Postfix queue control python tool (pyqueue)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of pyqueue
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

import os
from distutils.core import setup

if __name__ == '__main__':
    setup(
        name = "pyqueue",
        version = "0.5",
        url = "https://github.com/outini/pyqueue",
        author = "Denis Pompilio (jawa)",
        author_email = "denis.pompilio@gmail.com",
        maintainer = "Denis Pompilio (jawa)",
        maintainer_email = "denis.pompilio@gmail.com",
        description = "Postfix queue control python tool",
        long_description = file(os.path.join(os.path.dirname(__file__),
                                             'README.md')).read(),
        license = "GPLv2",
        platforms = ['UNIX'],
        packages = ['pyqueue'],
        package_dir = {'pyqueue': 'pyqueue'},
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
