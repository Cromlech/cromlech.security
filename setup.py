# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


version = '1.0'

install_requires = [
    'setuptools',
    'zope.security',
    'zope.interface',
    ]

tests_require = [
    'pytest',
    ]

setup(name='cromlech.security',
      version=version,
      description="Security layer for Cromlech to handle user/group policies.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='cromlech security',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
