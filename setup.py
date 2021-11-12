#!/usr/bin/env python

from distutils.core import setup

setup(name='bgfactory',
      version='0.1',
      description='Board Game Factory - a framework for composing reusable vector graphics assets, e.g. for board games',
      author='Adam Volný',
      author_email='adam.volny@gmail.com',
      # url='https://www.python.org/sigs/distutils-sig/',
      packages=['bgfactory', 'bgfactory.common', 'bgfactory.components'],
      package_dir = {'': 'src'},
      # url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
      # download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
      keywords=['board', 'game', 'factory', 'bgf', 'vector', 'graphics'],  # Keywords that define your package best
      install_requires=[  # I get to this in a second
            'cairocffi'
            'pangocffi',
            'pillow'
      ],
      classifiers=[
            'Development Status :: 3 - Alpha',
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Graphics :: Vector Graphics',
            'License :: OSI Approved :: MIT License',  # Again, pick a license
            # 'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
            # 'Programming Language :: Python :: 3.4',
            # 'Programming Language :: Python :: 3.5',
            # 'Programming Language :: Python :: 3.6',
      ],
     )