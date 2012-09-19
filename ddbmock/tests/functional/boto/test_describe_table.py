# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME = 'Table-1'
TABLE_NAME_404= 'Waldo'
TABLE_RT = 45
TABLE_WT = 123
TABLE_HK_NAME = u'hash_key'
TABLE_HK_TYPE = u'N'
TABLE_RK_NAME = u'range_key'
TABLE_RK_TYPE = u'S'

class TestDescribeTables(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        db = DynamoDB()
        db.hard_reset()

        hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
        range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

        t1 = Table(TABLE_NAME, TABLE_RT, TABLE_WT, hash_key, range_key)

        db.data[TABLE_NAME] = t1

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_describe_table(self):
        from ddbmock import connect_boto
        db = connect_boto()

        table = db.get_table(TABLE_NAME)

        self.assertEqual(TABLE_NAME, table.name)
        self.assertEqual(TABLE_RT, table.read_units)
        self.assertEqual(TABLE_WT, table.write_units)
        self.assertEqual(u'ACTIVE', table.status)
        self.assertEqual(TABLE_HK_NAME, table.schema.hash_key_name)
        self.assertEqual(TABLE_HK_TYPE, table.schema.hash_key_type)
        self.assertEqual(TABLE_RK_NAME, table.schema.range_key_name)
        self.assertEqual(TABLE_RK_TYPE, table.schema.range_key_type)

    def describe_table_404(self):
        from ddbmock import connect_boto
        db = connect_boto()

        self.assertRaises(DDBValidationErr, db.get_table,
            TABLE_NAME_404,
        )

