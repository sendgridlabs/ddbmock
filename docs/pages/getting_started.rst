##################################
Getting started with DynamoDB-Mock
##################################

.. include:: ../_include/intro.rst

Installation
============

::

    $ pip install ddbmock


Example usage
=============

Run as Regular client-server
----------------------------

Ideal for test environment. For stage and production I highly recommend using
DynamoDB servers. ddbmock comes with no warranty and *will* **loose your data(tm)**.

Launch the server

::

    $ pserve development.ini # launch the server on 0.0.0.0:6543

Start the client

::

    import boto
    from ddbmock import connect_boto_network

    # Use the provided helper to connect your *own* endpoint
    db = connect_boto_network()

    # Done ! just use it wherever in your project as usual.
    db.list_tables() # get list of tables (empty at this stage)

Note: if you do not want to import ddbmock only for the helper, here is a
reference implementation:

::

    def connect_boto_network(host='localhost', port=6543):
        import boto
        from boto.regioninfo import RegionInfo
        endpoint = '{}:{}'.format(host, port)
        region = RegionInfo(name='ddbmock', endpoint=endpoint)
        return boto.connect_dynamodb(region=region, port=port, is_secure=False)

Run as a standalone library
---------------------------

Ideal for unit testing or small scale automated functional tests. Nice to play
around with boto DynamoDB API too :)

::

    import boto
    from ddbmock import connect_boto_patch

    # Wire-up boto and ddbmock together
    db = connect_boto_patch()

    # Done ! just use it wherever in your project as usual.
    db.list_tables() # get list of tables (empty at this stage)

Note, to clean patches made in ``boto.dynamodb.layer1``, you can call
``clean_boto_patch()`` from  the same module.

Using ddbmock for tests
=======================

Most tests share the same structure:

 1. Set the things up
 2. Test and validate
 3. Clean everything up and start again

If you use ``ddbmock`` as a standalone library (which I recommend for this
purpose), feel free to access any of the public methods in the ``database`` and
``table`` to perform direct checks

Here is a template taken from ``GetItem`` functional test using Boto.

::

    # -*- coding: utf-8 -*-

    import unittest
    import boto

    TABLE_NAME = 'Table-HR'
    TABLE_RT = 45
    TABLE_WT = 123
    TABLE_HK_NAME = u'hash_key'
    TABLE_HK_TYPE = u'N'
    TABLE_RK_NAME = u'range_key'
    TABLE_RK_TYPE = u'S'

    HK_VALUE = u'123'
    RK_VALUE = u'Decode this data if you are a coder'


    ITEM = {
        TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
        TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE},
        u'relevant_data': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='},
    }

    class TestGetItem(unittest.TestCase):
        def setUp(self):
            from ddbmock import connect_boto_patch
            from ddbmock.database.db import dynamodb
            from ddbmock.database.table import Table
            from ddbmock.database.key import PrimaryKey

            # Do a full database wipe
            dynamodb.hard_reset()

            # Instanciate the keys
            hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
            range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

            # Create a test table and register it in ``self`` so that you can use it directly
            self.t1 = Table(TABLE_NAME, TABLE_RT, TABLE_WT, hash_key, range_key)

            # Very important: register the table in the DB
            dynamodb.data[TABLE_NAME]  = self.t1

            # Unconditionally add some data, for example.
            self.t1.put(ITEM, {})

            # Create the database connection ie: patch boto
            self.db = connect_boto_patch()

        def tearDown(self):
            from ddbmock.database.db import dynamodb
            from ddbmock import clean_boto_patch

            # Do a full database wipe
            dynamodb.hard_reset()

            # Remove the patch from Boto code (if any)
            clean_boto_patch()

        def test_get_hr(self):
            from ddbmock.database.db import dynamodb

            # Example test
            expected = {
                u'ConsumedCapacityUnits': 0.5,
                u'Item': ITEM,
            }

            key = {
                u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
                u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE},
            }

            # Example chech
            self.assertEquals(expected, self.db.layer1.get_item(TABLE_NAME, key))


If ddbmock is used as a standalone server, restarting it should do the job, unless
SQLite persistence is used.


Advanced usage
==============

A significant part of ddbmock is now configurable through ``ddbmock.config``
parameters. This includes the storage backend.

By default, ddbmock has no persitence and stores everything in-memory. Alternatively,
you can use the ``SQLite`` storage engine but be warned that it will be slower.
To switch the backend, you will to change a configuration variable *before* creating
the first table.

::

    from ddbmock import config

    # switch to sqlite backend
    config.STORAGE_ENGINE_NAME = 'sqlite'
    # define the database path. defaults to 'dynamo.db'
    config.STORAGE_SQLITE_FILE = '/tmp/my_database.sqlite'


Please note that ddbmock does not persist table metadata currently. As a
consequence, you will need to create the tables at each restart even with the
SQLite backend. This is hoped to be improved in future releases.

See https://bitbucket.org/Ludia/dynamodb-mock/src/tip/ddbmock/config.py for a full
list of parameters.
