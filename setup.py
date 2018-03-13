#!/usr/bin/env python
# because pkg_resources is slow
# also see https://github.com/pypa/setuptools/issues/510
from setuptools import setup, find_packages

setup(name='mlt',
      description='Machine Learning Container Tool',
      long_description=open('README.md').read(),
      author='Intel Nervana',
      author_email='intelnervana@intel.com',
      url='http://www.intelnervana.com',
      packages=find_packages(exclude=["tests"]),
      entry_points={
          'console_scripts': ['mlt=mlt.main:main']
      },
      package_data={
          'mlt': ['../templates']
      },
      include_package_data=True,
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
