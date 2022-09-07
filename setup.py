#!/usr/bin/env python3
""" LPlot is a generic command line plotting tool written in Python

- It provides a generic backend that can be interfaced with multiple
  plotting engines. Currently matplotlib is supported.
- It also supports saving and loading configurations into/from a file,
  making repeated plotting much easier.
"""
DOCLINES = (__doc__ or '').split("\n")

from setuptools import setup

# Using the versioneer to set the version of the distribution
import versioneer


if __name__ == '__main__':
  name = 'lplot'
  setup(name=name,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Lyuwen Fu',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    requires=['numpy', 'PyYAML', 'matplotlib'],
    provides=['lplot'],
    )
