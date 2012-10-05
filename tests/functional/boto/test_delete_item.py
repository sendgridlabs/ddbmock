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
    u'relevant_data': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='},
}

class TestDeleteItem(unittest.TestCase):
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

        self.t1.put(ITEM, {})
        self.t2.put(ITEM2, {})

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_delete_item_hr(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
            u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE},
        }

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
            },
            db.layer1.delete_item(TABLE_NAME, key),
        )
        self.assertEqual({}, self.t1.data[HK_VALUE][RK_VALUE])

    def test_delete_item_hr_old(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        expected = {
            u'ConsumedCapacityUnits': 1,
            u'Attributes': ITEM,
        }

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
            u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE},
        }

        self.assertEqual(
            expected,
            db.layer1.delete_item(TABLE_NAME, key, return_values=u'ALL_OLD'),
        )
        self.assertEqual({}, self.t1.data[HK_VALUE][RK_VALUE])

    def test_delete_item_h(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
        }

        self.assertEqual({
                u'ConsumedCapacityUnits': 1,
            },
            db.layer1.delete_item(TABLE_NAME2, key),
        )
        self.assertEqual({}, self.t2.data[HK_VALUE][False])

    def test_delete_item_h_old(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        db = connect_boto()

        expected = {
            u'ConsumedCapacityUnits': 1,
            u'Attributes': ITEM2,
        }

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
        }

        self.assertEqual(
            expected,
            db.layer1.delete_item(TABLE_NAME2, key, return_values=u'ALL_OLD'),
        )
        self.assertEqual({}, self.t1.data[HK_VALUE][False])

    def test_delete_item_hr_missing_r(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.dynamodb.exceptions import DynamoDBValidationError

        db = connect_boto()

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
        }

        self.assertRaises(DynamoDBValidationError,
                          db.layer1.delete_item,
                          TABLE_NAME, key)

    def test_delete_item_h_missing_h(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.dynamodb.exceptions import DynamoDBValidationError

        db = connect_boto()

        key = {}

        self.assertRaises(DynamoDBValidationError,
                          db.layer1.delete_item,
                          TABLE_NAME2, key)

    def test_delete_item_h_expect_field_value_ok(self):
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

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
            u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE},
        }

        db.layer1.delete_item(TABLE_NAME, key, expected=ddb_expected)
        self.assertEqual({}, self.t1.data[HK_VALUE][RK_VALUE])

    def test_delete_item_h_expect_field_value_fail(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB
        from boto.exception import DynamoDBResponseError

        db = connect_boto()

        ddb_expected = {
            u'relevant_data_et_bah_non': {
                u'Exists': True,
                u'Value': {u'B': u'THVkaWEgaXMgdGhlIGJlc3QgY29tcGFueSBldmVyIQ=='}
            }
        }

        key = {
            u"HashKeyElement":  {TABLE_HK_TYPE: HK_VALUE},
            u"RangeKeyElement": {TABLE_RK_TYPE: RK_VALUE},
        }

        self.assertRaisesRegexp(DynamoDBResponseError, 'ConditionalCheckFailedException',
            db.layer1.delete_item,
            TABLE_NAME, key, expected=ddb_expected
        )
        self.assertEqual(ITEM, self.t1.data[HK_VALUE][RK_VALUE])
