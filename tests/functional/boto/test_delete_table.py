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

class TestDeleteTables(unittest.TestCase):
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

    def test_delete(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        db.layer1.delete_table(TABLE_NAME)

        data = DynamoDB().data
        assert TABLE_NAME not in DynamoDB().data

    def test_delete_404(self):
        from ddbmock import connect_boto
        from boto.exception import BotoServerError

        db = connect_boto()

        self.assertRaises(BotoServerError, db.layer1.delete_table,
                          TABLE_NAME_404,
                         )
