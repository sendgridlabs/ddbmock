import unittest, mock, json, time

NOW = time.time()

TABLE_NAME1 = 'Table-1'
TABLE_NAME2 = 'Table-2'
TABLE_NAME_INVALID1 = 'Table-invalid 1'

TABLE_RT = 45
TABLE_WT = 123

HASH_KEY = {"AttributeName":"hash_key","AttributeType":"N"}
RANGE_KEY = {"AttributeName":"range_key","AttributeType":"S"}

HEADERS = {
    'x-amz-target': 'DynamoDB_20111205.CreateTable',
    'content-type': 'application/x-amz-json-1.0',
}

# Goal here is not to test the full API, this is done by the Boto tests
class TestCreateTable(unittest.TestCase):
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

    @mock.patch("ddbmock.database.table.time")
    def test_create_table_hr(self, m_time):
        from ddbmock.database.db import DynamoDB

        m_time.time.return_value = NOW

        request = {
            "TableName": TABLE_NAME1,
            "KeySchema": {
                "HashKeyElement": HASH_KEY,
                "RangeKeyElement": RANGE_KEY,
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": TABLE_RT,
                "WriteCapacityUnits": TABLE_WT,
            }
        }

        expected = {
            u'TableDescription': {
                u'CreationDateTime': NOW,
                u'KeySchema': {
                    u'HashKeyElement': HASH_KEY,
                    u'RangeKeyElement': RANGE_KEY,
                },
                u'ProvisionedThroughput': {
                    u'ReadCapacityUnits': TABLE_RT,
                    u'WriteCapacityUnits': TABLE_WT,
                },
                u'TableName': TABLE_NAME1,
                u'TableStatus': u'CREATING',
            }
        }

        res = self.app.post_json('/', request, HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8', res.headers['Content-Type'])

        data = DynamoDB().data
        assert TABLE_NAME1 in data
        table = data[TABLE_NAME1]

        self.assertEqual(TABLE_NAME1, table.name)
        self.assertEqual(TABLE_RT, table.rt)
        self.assertEqual(TABLE_WT, table.wt)
        self.assertEqual(NOW, table.creation_time)
        self.assertEqual(HASH_KEY['AttributeName'], table.hash_key.name)
        self.assertEqual(RANGE_KEY['AttributeName'], table.range_key.name)
        self.assertEqual(HASH_KEY['AttributeType'], table.hash_key.typename)
        self.assertEqual(RANGE_KEY['AttributeType'], table.range_key.typename)
