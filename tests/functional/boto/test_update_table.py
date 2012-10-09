# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME = 'Table-1'
TABLE_NAME_404 = 'Waldo'
TABLE_RT = 45
TABLE_WT = 123
TABLE_RT2 = 10
TABLE_WT2 = 200
TABLE_RT3 = 10
TABLE_WT3 = 2564756456
TABLE_HK_NAME = u'hash_key'
TABLE_HK_TYPE = u'N'
TABLE_RK_NAME = u'range_key'
TABLE_RK_TYPE = u'S'

class TestUpdateTables(unittest.TestCase):
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

    def test_update(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        db.layer1.update_table(TABLE_NAME, {'ReadCapacityUnits': TABLE_RT2,
                                            'WriteCapacityUnits': TABLE_WT2})

        data = DynamoDB().data
        assert TABLE_NAME in DynamoDB().data
        table = DynamoDB().data[TABLE_NAME]

        self.assertEqual(TABLE_NAME, table.name)
        self.assertEqual(TABLE_RT2, table.rt)
        self.assertEqual(TABLE_WT2, table.wt)

    def test_update_404(self):
        from ddbmock import connect_boto
        from boto.exception import BotoServerError

        db = connect_boto()

        self.assertRaises(BotoServerError, db.layer1.update_table,
                          TABLE_NAME_404,
                          {'ReadCapacityUnits': TABLE_RT2,
                           'WriteCapacityUnits': TABLE_WT2},
                         )

    def test_update_limite_exceeded_propagates(self):
        from ddbmock import connect_boto
        from boto.exception import BotoServerError

        db = connect_boto()

        self.assertRaises(BotoServerError, db.layer1.update_table,
                          TABLE_NAME,
                          {'ReadCapacityUnits': TABLE_RT3,
                           'WriteCapacityUnits': TABLE_WT3},
                         )

