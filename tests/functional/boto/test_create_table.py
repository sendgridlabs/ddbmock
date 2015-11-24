# -*- coding: utf-8 -*-

import unittest
import boto
from boto.dynamodb2.fields import HashKey, RangeKey

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'
TABLE_NAME3 = 'Table-3'
TABLE_NAME4 = 'Table-4'
TABLE_NAME_INVALID1 = 'Table-invalid 1'

TABLE_RT = 45
TABLE_WT = 123

TABLE_SCHEMA1 = {
    HashKey("hash_key"),
    RangeKey("range_key")
}

TABLE_SCHEMA2 = {
    HashKey("hash_key"),
}

TABLE_SCHEMA_INVALID1 = {
    HashKey("hash_key"),
}

# Not much can be tested here as most bugs are caught by Boto :)

@unittest.skip("Boto doesn't do the right schema anymore")
class TestCreateTable(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import dynamodb
        dynamodb.hard_reset()

    def tearDown(self):
        from ddbmock.database.db import dynamodb
        from ddbmock import clean_boto_patch
        dynamodb.hard_reset()
        clean_boto_patch()

    def test_create_table_hash_range(self):
        from ddbmock import connect_boto_patch
        from ddbmock.database.db import dynamodb

        db = connect_boto_patch()

        table = db.create_table(
            name=TABLE_NAME1,
            schema=[x.schema() for x in TABLE_SCHEMA1],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        self.assertEqual(TABLE_NAME1, table.name)
        self.assertEqual(TABLE_RT, table.read_units)
        self.assertEqual(TABLE_WT, table.write_units)
        self.assertEqual(u'CREATING', table.status)
        self.assertEqual(TABLE_SCHEMA1['hash_key_name'], table.schema.hash_key_name)
        self.assertEqual(TABLE_SCHEMA1['range_key_name'], table.schema.range_key_name)
        self.assertEqual(u'N', table.schema.hash_key_type)
        self.assertEqual(u'S', table.schema.range_key_type)

        data = dynamodb.data
        assert TABLE_NAME1 in data
        table = data[TABLE_NAME1]

        self.assertEqual(TABLE_NAME1, table.name)
        self.assertEqual(TABLE_RT, table.rt)
        self.assertEqual(TABLE_WT, table.wt)
        self.assertEqual(TABLE_SCHEMA1['hash_key_name'], table.hash_key.name)
        self.assertEqual(TABLE_SCHEMA1['range_key_name'], table.range_key.name)
        self.assertEqual(u'N', table.hash_key.typename)
        self.assertEqual(u'S', table.range_key.typename)

    def test_create_table_hash(self):
        from ddbmock import connect_boto_patch
        from ddbmock.database.db import dynamodb

        db = connect_boto_patch()

        table = db.create_table(
            name=TABLE_NAME2,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        self.assertEqual(TABLE_NAME2, table.name)
        self.assertEqual(TABLE_RT, table.read_units)
        self.assertEqual(TABLE_WT, table.write_units)
        self.assertEqual(u'CREATING', table.status)
        self.assertEqual(TABLE_SCHEMA2['hash_key_name'], table.schema.hash_key_name)
        self.assertEqual(u'N', table.schema.hash_key_type)
        self.assertIsNone(table.schema.range_key_name)
        self.assertIsNone(table.schema.range_key_type)

        data = dynamodb.data
        assert TABLE_NAME2 in data
        table = data[TABLE_NAME2]

        self.assertEqual(TABLE_NAME2, table.name)
        self.assertEqual(TABLE_RT, table.rt)
        self.assertEqual(TABLE_WT, table.wt)
        self.assertEqual(TABLE_SCHEMA2['hash_key_name'], table.hash_key.name)
        self.assertEqual(u'N', table.hash_key.typename)
        self.assertIsNone(table.range_key)

    def test_create_table_twice_fails(self):
        from ddbmock import connect_boto_patch
        from ddbmock.database.db import dynamodb
        from boto.exception import DynamoDBResponseError

        db = connect_boto_patch()

        #1st
        db.create_table(
            name=TABLE_NAME2,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        #2nd
        self.assertRaisesRegexp(DynamoDBResponseError, 'ResourceInUseException',
        db.create_table,
            name=TABLE_NAME2,
            schema=db.create_schema(**TABLE_SCHEMA2),
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )


    def test_create_table_invalid_name(self):
        from ddbmock import connect_boto_patch
        from ddbmock.database.db import dynamodb
        from boto.dynamodb.exceptions import DynamoDBValidationError as DDBValidationErr

        db = connect_boto_patch()

        assert TABLE_NAME_INVALID1 not in dynamodb.data

        self.assertRaises(DDBValidationErr, db.create_table,
            name=TABLE_NAME_INVALID1,
            schema=[x.schema() for x in TABLE_SCHEMA_INVALID1],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

    def test_create_table_reach_max(self):
        from ddbmock import connect_boto_patch, config
        from boto.exception import DynamoDBResponseError

        BK = config.MAX_TABLES
        config.MAX_TABLES = 3

        db = connect_boto_patch()

        #1
        db.create_table(
            name=TABLE_NAME1,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        #2
        db.create_table(
            name=TABLE_NAME2,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        #3
        db.create_table(
            name=TABLE_NAME3,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        #4
        self.assertRaisesRegexp(DynamoDBResponseError, 'LimitExceededException',
        db.create_table,
            name=TABLE_NAME4,
            schema=[x.schema() for x in TABLE_SCHEMA2],
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        #restore max
        config.MAX_TABLES = BK
