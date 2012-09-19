# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'
TABLE_NAME_INVALID1 = 'Table-invalid 1'

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

class TestListTables(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_create_table_hash_range(self):
        from ddbmock import connect_boto
        db = connect_boto()

        table = db.create_table(
            name=TABLE_NAME1,
            schema=db.create_schema(**TABLE_SCHEMA1),
            read_units=10,
            write_units=10,
        )

        self.assertEqual(TABLE_NAME1, table.name)

    def test_create_table_hash(self):
        from ddbmock import connect_boto
        db = connect_boto()

        table = db.create_table(
            name=TABLE_NAME2,
            schema=db.create_schema(**TABLE_SCHEMA2),
            read_units=10,
            write_units=10,
        )

        self.assertEqual(TABLE_NAME2, table.name)

    def test_create_table_invalid_name(self):
        from ddbmock import connect_boto
        from boto.dynamodb.exceptions import DynamoDBValidationError as DDBValidationErr

        db = connect_boto()

        self.assertRaises(DDBValidationErr, db.create_table,
            name=TABLE_NAME_INVALID1,
            schema=db.create_schema(**TABLE_SCHEMA_INVALID1),
            read_units=10,
            write_units=10,
        )
