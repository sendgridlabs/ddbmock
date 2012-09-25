# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME = 'Table-HR'
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

HK_VALUE = u'123'
RK_VALUE = u'Decode this data if you are a coder'


ITEM = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE},
    u'relevant_data': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='},
}
ITEM2 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE},
    u'irelevant_data': {u'B': u'WW91IHdpc2ggeW91IGNvdWxkIGNoYW5nZSB5b3VyIGpvYi4uLg=='},
}
ITEM3 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    u'relevant_data': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='},
}
ITEM4 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    u'irelevant_data': {u'B': u'WW91IHdpc2ggeW91IGNvdWxkIGNoYW5nZSB5b3VyIGpvYi4uLg=='},
}
ITEM5 = {
    u'relevant_data': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='},
}

class TestPutItem(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        db = DynamoDB()
        db.hard_reset()

        hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
        range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

        self.t1 = Table(TABLE_NAME, TABLE_RT, TABLE_WT, hash_key, range_key)
        self.t2 = Table(TABLE_NAME2, TABLE_RT, TABLE_WT, hash_key, None)

        db.data[TABLE_NAME]  = self.t1
        db.data[TABLE_NAME2] = self.t2

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    # TODO test with expected

    def test_put_hr(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
            },
            db.layer1.put_item(TABLE_NAME, ITEM),
        )
        self.assertEqual(ITEM, self.t1.data[HK_VALUE][RK_VALUE])

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
                u'Attributes': ITEM,
            },
            db.layer1.put_item(TABLE_NAME, ITEM2, return_values=u'ALL_OLD'),
        )

    def test_put_h(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
            },
            db.layer1.put_item(TABLE_NAME2, ITEM3),
        )
        self.assertEqual(ITEM3, self.t2.data[HK_VALUE][False])

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
                u'Attributes': ITEM3,
            },
            db.layer1.put_item(TABLE_NAME2, ITEM4, return_values=u'ALL_OLD'),
        )

    def test_put_hr_404(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.exception import DynamoDBResponseError

        db = connect_boto()

        self.assertRaisesRegexp(DynamoDBResponseError, 'ResourceNotFoundException',
                                db.layer1.put_item,
                                TABLE_NAME_404, ITEM)

    def test_put_h_404(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.exception import DynamoDBResponseError

        db = connect_boto()

        self.assertRaisesRegexp(DynamoDBResponseError, 'ResourceNotFoundException',
                                db.layer1.put_item,
                                TABLE_NAME_404, ITEM3)

    def test_put_hr_missing_r(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.dynamodb.exceptions import DynamoDBValidationError

        db = connect_boto()

        self.assertRaises(DynamoDBValidationError,
                          db.layer1.put_item,
                          TABLE_NAME, ITEM3)

    def test_put_h_missing_h(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.dynamodb.exceptions import DynamoDBValidationError

        db = connect_boto()

        self.assertRaises(DynamoDBValidationError,
                          db.layer1.put_item,
                          TABLE_NAME2, ITEM5)

    def test_put_h_expect_no_exist(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.exception import DynamoDBResponseError

        db = connect_boto()

        ddb_expected = {
            TABLE_HK_NAME: {u'Exists': False}
        }

        db.layer1.put_item(TABLE_NAME2, ITEM3, expected=ddb_expected)

        self.assertRaisesRegexp(DynamoDBResponseError, 'ConditionalCheckFailedException',
            db.layer1.put_item,
            TABLE_NAME2, ITEM4, expected=ddb_expected
        )
        self.assertEqual(ITEM3, self.t2.data[HK_VALUE][False])

    def test_put_h_expect_field_value(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.exception import DynamoDBResponseError

        db = connect_boto()

        ddb_expected = {
            u'relevant_data': {
                u'Exists': True,
                u'Value': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='}
            }
        }

        db.layer1.put_item(TABLE_NAME2, ITEM3)
        self.assertEqual(ITEM3, self.t2.data[HK_VALUE][False])
        db.layer1.put_item(TABLE_NAME2, ITEM4, expected=ddb_expected)
        self.assertEqual(ITEM4, self.t2.data[HK_VALUE][False])
        self.assertRaisesRegexp(DynamoDBResponseError, 'ConditionalCheckFailedException',
            db.layer1.put_item,
            TABLE_NAME2, ITEM4, expected=ddb_expected
        )
