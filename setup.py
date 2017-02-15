# -*- coding: utf-8 -*-
"""
pyknow setup script.

"""
from setuptools import setup, find_packages
import os

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()
NEWS = open(os.path.join(HERE, 'TODO.rst')).read()

VERSION = '0.1.4'

setup(name='pyknow',
      version=VERSION,
      description="Pure Python knowledge-based inference engine (inspired by CLIPS)",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
      keywords='knowledge-based inference engine',
      author='Roberto Abdelkader Martínez Pérez',
      author_email='rmartinez@buguroo.com',
      url='https://github.com/buguroo/pyknow',
      license='LGPLv3',
      packages=find_packages(exclude=["tests", "docs"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ])
