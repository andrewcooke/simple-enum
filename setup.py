
from distutils.core import setup

setup(
    name = 'simple-enum',
    url = 'https://github.com/andrewcooke/simple-enum',
    packages = ['simplenum'],
    package_dir = {'': 'src'},
    version = '0.0.1',
    description = 'A simpler Enum for Python 3',
    author = 'Andrew Cooke',
    author_email = 'andrew@acooke.org',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: Public Domain',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries'],
    long_description = '''
What Does Simple Enum Do?
--------------------------

Simple Enum provides a simpler way to define Enums in Python 3::

    class Colour(Enum):
        red
        green
        blue

You can see the full documentation (and implementation) on
`github <https://github.com/andrewcooke/simple-enum>`_.

Why Should I Use Simple Enum?
------------------------------

* It makes the common case as simple as possible.

* It detects accidental duplicate values.

* It allows you to easily select alternative values (numbers from one, bit
  fields, etc).

What Else Should I Know?
------------------------

* (c) 2013 Andrew Cooke, andrew@acooke.org; released into the public domain
  for any use, but with absolutely no warranty.
    '''
)
