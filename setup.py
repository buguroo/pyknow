# -*- coding: utf-8 -*-
"""
pyknow setup script.

"""
from setuptools import setup, find_packages
import os

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()
NEWS = open(os.path.join(HERE, 'TODO.rst')).read()

VERSION = '1.7.0'

setup(name='pyknow',
      version=VERSION,
      description="PyKnow: Expert Systems for Python",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      keywords='knowledge-based inference engine',
      author='Roberto Abdelkader Martínez Pérez',
      author_email='robertomartinezp@gmail.com',
      url='https://github.com/buguroo/pyknow',
      license='LGPLv3',
      packages=find_packages(exclude=["tests", "docs"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'frozendict==1.2',
        'schema==0.6.7'
      ])
