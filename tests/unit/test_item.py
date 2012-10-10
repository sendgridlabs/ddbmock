# -*- coding: utf-8 -*-

import unittest

# tests
# - actions
# - expected values

FIELDNAME = "fieldname"
VALUE_S = {"S": "String value"}
VALUE_N = {"N": "123"}
VALUE_B = {"B": "QmluYXJ5IGRhdGE="}
VALUE_SS = {"SS": ["String value", "Ludia", "Waldo"]}
VALUE_NS = {"NS": ["456", "789"]}
VALUE_BS = {"BS": ["QmluYXJ5IGRhdGE="]}

VALUE_SS_DEL = {"SS": ["Ludia", "zinga"]}
VALUE_SS_SUR = {"SS": ["String value", "Waldo"]}
VALUE_SS_RES = {"SS": ['Ludia', 'String value', 'zinga', 'Waldo']}
VALUE_N_X2 = {"N": "246"}

class TestItem(unittest.TestCase):
    # actions
    def test_action_put(self):
        from ddbmock.database.item import Item

        # explicit
        item = Item({})
        item._apply_action(FIELDNAME, {"Action": "PUT", "Value": VALUE_S})
        self.assertEqual([(FIELDNAME, VALUE_S)], item.items())

        # implicit
        item = Item({})
        item._apply_action(FIELDNAME, {"Value": VALUE_S})
        self.assertEqual([(FIELDNAME, VALUE_S)], item.items())

    def test_action_delete(self):
        from ddbmock.database.item import Item

        # field does not exist (just ignores)
        item = Item({})
        item._apply_action(FIELDNAME, {"Action": "DELETE", "Value": VALUE_S})
        self.assertEqual([], item.items())

        # delete scalar value
        item = Item({
            FIELDNAME: VALUE_S,
        })
        item._apply_action(FIELDNAME, {"Action": "DELETE"})
        self.assertEqual([], item.items())

        # delete set from set
        item = Item({
            FIELDNAME: VALUE_SS,
        })
        item._apply_action(FIELDNAME, {"Action": "DELETE", "Value": VALUE_SS_DEL})
        self.assertEqual([(FIELDNAME, VALUE_SS_SUR)], item.items())

        # delete set all from set
        item = Item({
            FIELDNAME: VALUE_SS,
        })
        item._apply_action(FIELDNAME, {"Action": "DELETE", "Value": VALUE_SS})
        self.assertEqual([], item.items())

    def test_action_add(self):
        from ddbmock.database.item import Item

        # add value to int field
        item = Item({FIELDNAME: VALUE_N})
        item._apply_action(FIELDNAME, {"Action": "ADD", "Value": VALUE_N})
        self.assertEqual([(FIELDNAME, VALUE_N_X2)], item.items())

        # push value to any set
        item = Item({FIELDNAME: VALUE_SS})
        item._apply_action(FIELDNAME, {"Action": "ADD", "Value": VALUE_SS_DEL})
        self.assertEqual([(FIELDNAME, VALUE_SS_RES)], item.items())

        # field does not exist
        item = Item({})
        item._apply_action(FIELDNAME, {"Action": "ADD", "Value": VALUE_NS})
        self.assertEqual([(FIELDNAME, VALUE_NS)], item.items())


    def test_action_type_mismatch(self):
        from ddbmock.database.item import Item

        # delete from set, set of same type
        item = Item({
            FIELDNAME: VALUE_SS,
        })
        self.assertRaises(TypeError,
                          item._apply_action,
                          FIELDNAME, {"Action": "DELETE", "Value": VALUE_S})
        self.assertEqual([(FIELDNAME, VALUE_SS)], item.items())
        self.assertRaises(TypeError,
                          item._apply_action,
                          FIELDNAME, {"Action": "DELETE", "Value": VALUE_NS})
        self.assertEqual([(FIELDNAME, VALUE_SS)], item.items())

        # delete value from scalar field (fail)
        item = Item({
            FIELDNAME: VALUE_S,
        })
        self.assertRaises(TypeError,
                          item._apply_action,
                          FIELDNAME, {"Action": "DELETE", "Value": VALUE_S})
        self.assertEqual([(FIELDNAME, VALUE_S)], item.items())

        # add to scalar non number field
        item = Item({FIELDNAME: VALUE_S})
        self.assertRaises(TypeError,
                          item._apply_action,
                          FIELDNAME, {"Action": "ADD", "Value": VALUE_S})
        self.assertEqual([(FIELDNAME, VALUE_S)], item.items())

        # add to set of different type
        item = Item({FIELDNAME: VALUE_SS})
        self.assertRaises(TypeError,
                          item._apply_action,
                          FIELDNAME, {"Action": "ADD", "Value": VALUE_NS})
        self.assertEqual([(FIELDNAME, VALUE_SS)], item.items())

        # add non number to non existing field
        item = Item({})
        self.assertRaises(ValueError,
                          item._apply_action,
                          FIELDNAME, {"Action": "ADD", "Value": VALUE_S})
        self.assertEqual([], item.items())

    def test_expected_field_does_not_exist(self):
        from ddbmock.database.item import Item
        from ddbmock.errors import ConditionalCheckFailedException

        # ok
        item = Item({})
        item.assert_match_expected({
           FIELDNAME: {u'Exists': False}
        })

        # mismatch
        item = Item({FIELDNAME: VALUE_SS})
        self.assertRaises(ConditionalCheckFailedException,
                          item.assert_match_expected,
                          {FIELDNAME: {u'Exists': False}})

    def test_expected_field_exists_value(self):
        from ddbmock.database.item import Item
        from ddbmock.errors import ConditionalCheckFailedException

        # ok
        item = Item({FIELDNAME: VALUE_S})
        item.assert_match_expected({
           FIELDNAME: {'Exists': True, 'Value': VALUE_S}
        })

        # exitence mismatch
        item = Item({})
        self.assertRaises(ConditionalCheckFailedException,
                          item.assert_match_expected,
                          {FIELDNAME: {'Exists': True, 'Value': VALUE_S}})

        # type mismatch
        item = Item({FIELDNAME: VALUE_S})
        self.assertRaises(ConditionalCheckFailedException,
                          item.assert_match_expected,
                          {FIELDNAME: {'Exists': True, 'Value': VALUE_N}})
