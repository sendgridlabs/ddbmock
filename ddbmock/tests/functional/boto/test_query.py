# -*- coding: utf-8 -*-

import unittest
import boto

TABLE_NAME = 'Table-HR'
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
RK_VALUE1 = u'Waldo-1'
RK_VALUE2 = u'Waldo-2'
RK_VALUE3 = u'Waldo-3'
RK_VALUE4 = u'Waldo-4'
RK_VALUE5 = u'Waldo-5'


ITEM1 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE1},
    u'relevant_data': {u'S': u'tata'},
}
ITEM2 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE2},
    u'relevant_data': {u'S': u'tete'},
}
ITEM3 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE3},
    u'relevant_data': {u'S': u'titi'},
}
ITEM4 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE4},
    u'relevant_data': {u'S': u'toto'},
}
ITEM5 = {
    TABLE_HK_NAME: {TABLE_HK_TYPE: HK_VALUE},
    TABLE_RK_NAME: {TABLE_RK_TYPE: RK_VALUE5},
    u'relevant_data': {u'S': u'tutu'},
}

# Please note that most query features are not yet implemented hence not tested
class TestQuery(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import DynamoDB
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        db = DynamoDB()
        db.hard_reset()

        hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
        range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

        self.t1 = Table(TABLE_NAME, TABLE_RT, TABLE_WT, hash_key, range_key)

        db.data[TABLE_NAME]  = self.t1

        self.t1.put(ITEM1, {})
        self.t1.put(ITEM2, {})
        self.t1.put(ITEM3, {})
        self.t1.put(ITEM4, {})
        self.t1.put(ITEM5, {})

    def tearDown(self):
        from ddbmock.database.db import DynamoDB
        DynamoDB().hard_reset()

    def test_query_all(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        expected = {
            u"Count": 5,
            u"Items": [
                {u"relevant_data": {u"S": u"titi"}, u"hash_key": {u"N": u"123"}, u"range_key": {u"S": u"Waldo-3"}},
                {u"relevant_data": {u"S": u"tete"}, u"hash_key": {u"N": u"123"}, u"range_key": {u"S": u"Waldo-2"}},
                {u"relevant_data": {u"S": u"tata"}, u"hash_key": {u"N": u"123"}, u"range_key": {u"S": u"Waldo-1"}},
                {u"relevant_data": {u"S": u"tutu"}, u"hash_key": {u"N": u"123"}, u"range_key": {u"S": u"Waldo-5"}},
                {u"relevant_data": {u"S": u"toto"}, u"hash_key": {u"N": u"123"}, u"range_key": {u"S": u"Waldo-4"}},
            ],
            u"ConsumedCapacityUnits": 2.5,
        }

        db = connect_boto()

        ret = db.layer1.query(TABLE_NAME, {TABLE_HK_TYPE: HK_VALUE})
        self.assertEqual(expected, ret)

    def test_query_all_filter_fields(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        expected = {
            u"Count": 5,
            u"Items": [
                {u"relevant_data": {u"S": "titi"}},
                {u"relevant_data": {u"S": "tete"}},
                {u"relevant_data": {u"S": "tata"}},
                {u"relevant_data": {u"S": "tutu"}},
                {u"relevant_data": {u"S": "toto"}},
            ],
            u"ConsumedCapacityUnits": 2.5,
        }
        fields = [u'relevant_data']

        db = connect_boto()

        ret = db.layer1.query(TABLE_NAME, {TABLE_HK_TYPE: HK_VALUE}, None, fields)
        self.assertEqual(expected, ret)

    # No need to test all conditions/type mismatch as they are unit tested
    def test_query_condition_filter_fields(self):
        from ddbmock import connect_boto
        from ddbmock.database.db import DynamoDB

        expected = {
            u"Count": 3,
            u"Items": [
                {u"relevant_data": {u"S": u"titi"}},
                {u"relevant_data": {u"S": u"tutu"}},
                {u"relevant_data": {u"S": u"toto"}},
            ],
            u"ConsumedCapacityUnits": 1.5,
        }

        condition = {"AttributeValueList":[{"S":"Waldo-2"}],"ComparisonOperator":"GT"}
        fields = [u'relevant_data']

        db = connect_boto()

        ret = db.layer1.query(TABLE_NAME, {TABLE_HK_TYPE: HK_VALUE}, condition, fields)
        self.assertEqual(expected, ret)

