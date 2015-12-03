import json
import unittest

TABLE_NAME1 = 'Table-HR'
TABLE_NAME2 = 'Table-H'
TABLE_NAME_404 = 'Waldo'
TABLE_RT = 45
TABLE_WT = 123
TABLE_RT2 = 10
TABLE_WT2 = 10
TABLE_HK_NAME = u'hash_key'
TABLE_HK_TYPE = u'N'
TABLE_RK_NAME = u'range_key'
TABLE_RK_TYPE = u'S'

HK_VALUE1 = u'123'
HK_VALUE2 = u'456'
HK_VALUE3 = u'789'
RK_VALUE1 = u'Waldo-1'
RK_VALUE2 = u'Waldo-2'
RK_VALUE3 = u'Waldo-3'
RK_VALUE4 = u'Waldo-4'
RK_VALUE5 = u'Waldo-5'


ITEM1 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE1},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE1},
    u'relevant_data': {u'S': u'tata'},
}
ITEM2 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE1},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE2},
    u'relevant_data': {u'S': u'tete'},
}
ITEM3 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE2},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE3},
    u'relevant_data': {u'S': u'titi'},
}
ITEM4 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE2},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE4},
    u'relevant_data': {u'S': u'toto'},
}
ITEM5 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE3},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE5},
    u'relevant_data': {u'S': u'tutu'},
}

HEADERS = {
    'x-amz-target': 'dynamodb_20111205.BatchGetItem',
    'content-type': 'application/x-amz-json-1.0',
}


# Goal here is not to test the full API, this is done by the Boto tests
class TestBatchGetItem(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import dynamodb
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        import helpers
        self.app = helpers.makeTestApp()

        dynamodb.hard_reset()

        hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
        range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

        self.t1 = Table(TABLE_NAME1, TABLE_RT, TABLE_WT, hash_key, range_key)
        self.t2 = Table(TABLE_NAME2, TABLE_RT, TABLE_WT, hash_key, None)

        dynamodb.data[TABLE_NAME1] = self.t1
        dynamodb.data[TABLE_NAME2] = self.t2

        self.t1.put(ITEM1, {})
        self.t1.put(ITEM2, {})
        self.t1.put(ITEM3, {})
        self.t2.put(ITEM4, {})
        self.t2.put(ITEM5, {})

    def tearDown(self):
        from ddbmock.database.db import dynamodb
        dynamodb.hard_reset()

    def test_batch_get_item_filter_one(self):
        request = {
            u"RequestItems": {
                TABLE_NAME1: {
                    u"Keys": [
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE1},
                         u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE1},
                         },
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE1},
                         u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE1}
                         },
                        ],
                    u"AttributesToGet": [u"relevant_data"],
                    },
                TABLE_NAME2: {
                    u"Keys": [
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE3}},
                        ],
                    },
                }
            }

        expected = {
            "Responses": {
                "Table-HR": {
                    "Items": [
                        {"relevant_data": {"S": "tata"}},
                        {"relevant_data": {"S": "tata"}},
                    ],
                    "ConsumedCapacityUnits": 1.0
                },
                "Table-H": {
                    "Items": [
                        {"relevant_data": {"S": "tutu"},
                         "hash_key": {"N": "789"},
                         "range_key": {"S": "Waldo-5"}
                         },
                    ],
                    "ConsumedCapacityUnits": 0.5
                }
            }
        }

        # Protocol check

        res = self.app.post_json('/', request, headers=HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])

    def test_batch_get_item_filter_one_consistent(self):
        request = {
            u"RequestItems": {
                TABLE_NAME1: {
                    u"Keys": [
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE1},
                         u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE1}
                         },
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE1},
                         u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE1}
                         },
                        ],
                    u"AttributesToGet": [u"relevant_data"],
                    u"ConsistentRead": True,
                },
                TABLE_NAME2: {
                    u"Keys": [
                        {u"HashKeyElement": {TABLE_HK_TYPE: HK_VALUE3}},
                    ],
                },
            }
        }

        expected = {
            "Responses": {
                "Table-HR": {
                    "Items": [
                        {"relevant_data": {"S": "tata"}},
                        {"relevant_data": {"S": "tata"}},
                    ],
                    "ConsumedCapacityUnits": 2.0
                },
                "Table-H": {
                    "Items": [
                        {"relevant_data": {"S": "tutu"},
                         "hash_key": {"N": "789"},
                         "range_key": {"S": "Waldo-5"}
                         },
                    ],
                    "ConsumedCapacityUnits": 0.5
                }
            }
        }

        # Protocol check
        res = self.app.post_json('/', request, headers=HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])
