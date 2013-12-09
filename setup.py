#!/usr/bin/env python
import sys

if 'develop' in sys.argv:
    # use setuptools for develop, but nothing else
    from setuptools import setup
else:
    from distutils.core import setup

from distutils.command.build_py import build_py

with open('README.rst') as file:
    long_description = file.read()

with open('CHANGES.rst') as file:
    long_description += file.read()


setup(name='casa_tools',
      version='0.1.0.dev',
      description='Python package to do various things with CASA; mostly a testbed for CASA development',
      author='Adam Ginsburg',
      author_email='adam.g.ginsburg@gmail.com',
      packages=['casa_tools'],
      provides=['casa_tools'],
      scripts=['scripts/hdr_freqtovel'],
      requires=['astropy'],
      cmdclass={'build_py': build_py},
      classifiers=["Development Status :: 3 - Alpha",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                   ],
      )
