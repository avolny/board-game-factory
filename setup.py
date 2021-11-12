#!/usr/bin/env python

from distutils.core import setup

setup(name='bgfactory',
      version='1.0',
      description='Board Game Factory',
      author='Adam Volný',
      author_email='adam.volny@gmail.com',
      # url='https://www.python.org/sigs/distutils-sig/',
      packages=['bgfactory', 'bgfactory.common', 'bgfactory.components'],
      package_dir = {'': 'src'}
     )