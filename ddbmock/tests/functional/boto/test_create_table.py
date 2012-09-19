# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'
TABLE_NAME_INVALID1 = 'Table-invalid 1'

TABLE_RT = 45
TABLE_WT = 123

TABLE_SCHEMA1 = {
    'hash_key_name': 'hash_key',
    'hash_key_proto_value': int,
    'range_key_name': 'range_key',
    'range_key_proto_value': unicode,
}

TABLE_SCHEMA2 = {
    'hash_key_name': 'hash_key',
    'hash_key_proto_value': int,
}

TABLE_SCHEMA_INVALID1 = {
    'hash_key_name': 'hash_key',
    'hash_key_proto_value': unicode,
}

# Not much can be tested here as most bugs are caught by Boto :)

class TestCreateTable(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_create_table_hash_range(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        table = db.create_table(
            name=TABLE_NAME1,
            schema=db.create_schema(**TABLE_SCHEMA1),
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        self.assertEqual(TABLE_NAME1, table.name)
        self.assertEqual(TABLE_RT, table.read_units)
        self.assertEqual(TABLE_WT, table.write_units)
        self.assertEqual(u'ACTIVE', table.status)
        self.assertEqual(TABLE_SCHEMA1['hash_key_name'], table.schema.hash_key_name)
        self.assertEqual(TABLE_SCHEMA1['range_key_name'], table.schema.range_key_name)
        self.assertEqual(u'N', table.schema.hash_key_type)
        self.assertEqual(u'S', table.schema.range_key_type)

        data = DynamoDB().data
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
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        table = db.create_table(
            name=TABLE_NAME2,
            schema=db.create_schema(**TABLE_SCHEMA2),
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )

        self.assertEqual(TABLE_NAME2, table.name)
        self.assertEqual(TABLE_RT, table.read_units)
        self.assertEqual(TABLE_WT, table.write_units)
        self.assertEqual(u'ACTIVE', table.status)
        self.assertEqual(TABLE_SCHEMA2['hash_key_name'], table.schema.hash_key_name)
        self.assertEqual(u'N', table.schema.hash_key_type)
        self.assertIsNone(table.schema.range_key_name)
        self.assertIsNone(table.schema.range_key_type)

        data = DynamoDB().data
        assert TABLE_NAME2 in data
        table = data[TABLE_NAME2]

        self.assertEqual(TABLE_NAME2, table.name)
        self.assertEqual(TABLE_RT, table.rt)
        self.assertEqual(TABLE_WT, table.wt)
        self.assertEqual(TABLE_SCHEMA2['hash_key_name'], table.hash_key.name)
        self.assertEqual(u'N', table.hash_key.typename)
        self.assertIsNone(table.range_key)


    def test_create_table_invalid_name(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.dynamodb.exceptions import DynamoDBValidationError as DDBValidationErr

        db = connect_boto()

        assert TABLE_NAME_INVALID1 not in DynamoDB().data

        self.assertRaises(DDBValidationErr, db.create_table,
            name=TABLE_NAME_INVALID1,
            schema=db.create_schema(**TABLE_SCHEMA_INVALID1),
            read_units=TABLE_RT,
            write_units=TABLE_WT,
        )
