#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mlt',
      description='Machine Learning Container Tool',
      long_description=open('README.md').read(),
      author='Intel Nervana',
      author_email='intelnervana@intel.com',
      url='http://www.intelnervana.com',
      scripts=['bin/mlt'],
      packages=find_packages(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: POSIX',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering :: ' +
                   'Artificial Intelligence',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Topic :: System :: Distributed Computing'])
