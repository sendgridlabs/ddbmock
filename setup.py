# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

install_requires = [
    'pyramid',
    'onctuous >= 0.5.1',
]

setup_requires = [
    'd2to1',
    'boto',
    'nose',
    'nosexcover',
    'coverage',
    'mock',
    'webtest',
]

setup(
    d2to1=True,
    keywords='pyramid dynamodb mock planification',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    test_suite='nose.collector',
    entry_points="""\
    [paste.app_factory]
    main = ddbmock:main
    """,
)
