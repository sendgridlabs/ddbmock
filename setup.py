
from setuptools import setup, find_packages

setup(
    d2to1=True,
    keywords='pyramid dynamodb mock planification',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['d2to1'],
    test_suite='nose.collector',
    entry_points="""\
    [paste.app_factory]
    main = ddbmock:main
    """,
)
