# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    # d2to1 bootstrap
    'd2to1',

    'pyramid',
    'waitress',
    'webtest',
    'voluptuous',
]

tests_requires = [
    # d2to1 bootstrap
    'd2to1',
    'voluptuous',
    'pyramid',
    'boto',

    'nose',
    'nosexcover',
    'coverage',
    'mock',
]

setup(name='ddbmock',
      d2to1=True,
      keywords='pyramid dynamodb mock',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_requires,
      test_suite="ddbmock",
      entry_points = """\
      [paste.app_factory]
      main = ddbmock:main
      """,
)

