############################
DynamoDB-mock documentation.
############################

Overview
========

.. include:: _include/intro.rst

What is ddbmock *not* useful for ?
----------------------------------

Do *not* use it in production or as a cheap DynamoDB replacement. I'll never
stress it enough.

All the focus was on simplicity/hackability and simulation quality. Nothing else.

What is ddbmock useful for ?
----------------------------

- FAST and RELIABLE unit testing
- FAST and RELIABLE functional testing
- experiment with DynamoDB API.
- RELIABLE throughput planification
- RELIABLE disk space planification
- almost any DynamoDB simulation !

ddbmock can also persist your data in SQLITE. This open another vast range of
possibilities :)

History
-------

 - v1.0.0 (*): full documentation and bugfixes
 - v0.4.1: schema persistence + thread safety, bugfixes
 - v0.4.0: sqlite backend + throughput statistics + refactoring, more documentation, more tests
 - v0.3.2: batchWriteItem support + pass boto integration tests
 - v0.3.1: accuracy in item/table sizes + full test coverage
 - v0.3.0: first public release. Full table lifecycle + most items operations

(?) indicates a future release. These are only ideas or "nice to have".

Documentation
=============

User guide
----------

.. toctree::
   :maxdepth: 3

   pages/getting_started
   pages/status
   pages/planning
   pages/extending

   pages/changelog

Database API
------------

Describe internal database structures. Should be extremely useful for tests.

.. toctree::
   :maxdepth: 4
   :glob:

   api/database/*


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contribute
==========

Want to contribute, report a but of request a feature ? The development goes on
BitBucket:

- **Download**: http://pypi.python.org/pypi/ddbmock
- **Report bugs**: https://bitbucket.org/Ludia/dynamodb-mock/issues
- **Fork the code**: https://bitbucket.org/Ludia/dynamodb-mock/overview
