# -*- coding: utf-8 -*-

import unittest, json

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'

HEADERS = {
    'x-amz-target': 'DynamoDB_20111205.ListTables',
    'content-type': 'application/x-amz-json-1.0',
}

class TestListTables(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        from ddbmock import main
        app = main({})
        from webtest import TestApp
        self.app = TestApp(app)

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

        request = {}

        expected = {
            "TableNames": [TABLE_NAME1, TABLE_NAME2],
        }

        res = self.app.post_json('/', request, HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8', res.headers['Content-Type'])

