# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'

class TestListTables(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        db = DynamoDB()
        db.hard_reset()

        hash_key = PrimaryKey('hash_key', 'N')
        range_key = PrimaryKey('range_key', 'S')

        t1 = Table(TABLE_NAME1, 10, 10, hash_key, range_key)
        t2 = Table(TABLE_NAME2, 10, 10, hash_key, range_key)

        db.data[TABLE_NAME1] = t1
        db.data[TABLE_NAME2] = t2

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_list_tables(self):
        from ddbmock import connect_boto
        db = connect_boto()

        expected = [TABLE_NAME1, TABLE_NAME2]

        self.assertEqual(expected, db.list_tables())

