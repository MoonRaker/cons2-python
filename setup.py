#!/usr/bin/env python

import os
import re
import shutil
import sys

try:
    from setuptools import setup, Command
    from setuptools.extension import Extension
except ImportError:
    raise RuntimeError('setuptools is required')


import versioneer


# DESCRIPTION = ('A set of functions and classes for simulating the ' +
#                'performance of photovoltaic energy systems.')
# LONG_DESCRIPTION = """
# PVLIB Python is a community supported tool that provides a set of
# functions and classes for simulating the performance of photovoltaic
# energy systems. PVLIB Python was originally ported from the PVLIB MATLAB
# toolbox developed at Sandia National Laboratories and it implements many
# of the models and methods developed at the Labs. More information on
# Sandia Labs PV performance modeling programs can be found at
# https://pvpmc.sandia.gov/. We collaborate with the PVLIB MATLAB project,
# but operate independently of it.

# We need your help to make pvlib-python a great tool!

# Documentation: http://pvlib-python.readthedocs.io

# Source code: https://github.com/pvlib/pvlib-python
# """

DISTNAME = 'cons2'
LICENSE = 'GNU GPLv3'
AUTHOR = 'CONS2 Python Developers'
MAINTAINER_EMAIL = 'derek.groenendyk@gmail.com'
URL = 'https://github.com/MoonRaker/cons2-python'

INSTALL_REQUIRES = ['numpy >= 1.9.0',
                    'pandas >= 0.14.0',
                    'six',
                    ]
TESTS_REQUIRE = ['pytest', 'nose']

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: GNU GPLv3 License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering',
]

setuptools_kwargs = {
    'zip_safe': False,
    'scripts': [],
    'include_package_data': True
}

# set up pvlib packages to be installed and extensions to be compiled
PACKAGES = ['cons2']

extensions = []

setup(name=DISTNAME,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
      tests_require=TESTS_REQUIRE,
      ext_modules=extensions,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      maintainer_email=MAINTAINER_EMAIL,
      license=LICENSE,
      url=URL,
      classifiers=CLASSIFIERS,
      **setuptools_kwargs)
