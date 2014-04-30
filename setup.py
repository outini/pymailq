import os
from distutils.core import setup
import pyqueue

# setup.py actually relies on py_module
# PyQueue will be refactored to become a package

setup(name="pyqueue",
      version=pyqueue.__version__,
      url="https://github.com/outini/pyqueue",
      author=pyqueue.__author__,
      author_email=pyqueue.__email__,
      maintainer=pyqueue.__author__,
      maintainer_email=pyqueue.__email__,
      description="Postfix queue control python tool",
      long_description=file(os.path.join(os.path.dirname(__file__),
                                         'README.md')).read(),
      license=pyqueue.__license__,
      platforms=['linux', 'bsd'],
      py_modules=['pyqueue', 'pyqueueshell'],
      classifiers=[
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
