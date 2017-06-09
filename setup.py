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


DESCRIPTION = ('A program for calculating consumptive use based on the Blaney-Criddle method')
LONG_DESCRIPTION = """
cons2-python is a library used to calculated consumptive use based on the Blaney-Criddle method.
It was originally written in FORTRAN and has been translated. Consumptive use using the Blaney-
Criddle method can be calculated using either SCS-NRCS or FAO crop coefficients. It has been
tested and compares well with the FORTRAN results. It has been used and tested but may need 
further evaluation.

Documentation: http://cons2-python.readthedocs.io

Source code: https://github.com/MoonRaker/cons2-python
"""

DISTNAME = 'cons2'
LICENSE = 'GNU GPLv3'
AUTHOR = 'CONS2 Python Developers'
MAINTAINER_EMAIL = 'derek.groenendyk@gmail.com'
URL = 'https://github.com/MoonRaker/cons2-python'

INSTALL_REQUIRES = ['numpy >= 1.9.0',
                    'pandas >= 0.14.0',
                    'six',
                    ]
# TESTS_REQUIRE = ['pytest', 'nose']
TESTS_REQUIRE = []

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

# set up cons2 packages to be installed and extensions to be compiled
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
