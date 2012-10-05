# -*- coding: utf-8 -*-

import unittest, json

TABLE_NAME1 = 'Table-1'

TABLE_RT = 45
TABLE_WT = 123

HASH_KEY = {"AttributeName":"hash_key","AttributeType":"N"}
RANGE_KEY = {"AttributeName":"range_key","AttributeType":"S"}

HEADERS = {
    'x-amz-target': 'DynamoDB_20111205.-----',
    'content-type': 'application/x-amz-json-1.0',
}

# Goal here is not to test the full API, this is done by the Boto tests
class TestTODO(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock import main
        app = main({})
        from webtest import TestApp
        self.app = TestApp(app)
        DynamoDB().hard_reset()

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_TODO(self):
        from ddbmock.database.db import DynamoDB

        request = {}
        expected = {}

        # Protocol check
        res = self.app.post_json('/', request, HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8', res.headers['Content-Type'])

        # Live data check
        data = DynamoDB().data
        assert TABLE_NAME1 in data
        table = data[TABLE_NAME1]

        self.assertEqual(TABLE_NAME1, table.name)
