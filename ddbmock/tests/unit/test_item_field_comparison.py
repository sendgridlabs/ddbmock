# -*- coding: utf-8 -*-

import unittest


class TestItemFieldComparison(unittest.TestCase):
    def test_eq(self):
        from ddbmock.database.comparison import eq

        self.assertTrue(eq({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertFalse(eq({u'S': u'waldo'}, {u'S': u'on-time'}))

    def test_le(self):
        from ddbmock.database.comparison import le

        self.assertTrue(le({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertTrue(le({u'S': u'waldo'}, {u'S': u'waldo1'}))
        self.assertFalse(le({u'S': u'waldo'}, {u'S': u'wald'}))

        self.assertTrue(le({u'N': u'42'}, {u'N': u'42'}))
        self.assertTrue(le({u'N': u'42'}, {u'N': u'42.001'}))
        self.assertFalse(le({u'N': u'42'}, {u'N': u'7'}))

    def test_lt(self):
        from ddbmock.database.comparison import lt

        self.assertFalse(lt({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertTrue(lt({u'S': u'waldo'}, {u'S': u'waldo1'}))
        self.assertFalse(lt({u'S': u'waldo'}, {u'S': u'wald'}))

        self.assertFalse(lt({u'N': u'42'}, {u'N': u'42'}))
        self.assertTrue(lt({u'N': u'42'}, {u'N': u'42.001'}))
        self.assertFalse(lt({u'N': u'42'}, {u'N': u'7'}))

    def test_ge(self):
        from ddbmock.database.comparison import ge

        self.assertTrue(ge({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertFalse(ge({u'S': u'waldo'}, {u'S': u'waldo1'}))
        self.assertTrue(ge({u'S': u'waldo'}, {u'S': u'wald'}))

        self.assertTrue(ge({u'N': u'42'}, {u'N': u'42'}))
        self.assertFalse(ge({u'N': u'42'}, {u'N': u'42.001'}))
        self.assertTrue(ge({u'N': u'42'}, {u'N': u'7'}))

    def test_gt(self):
        from ddbmock.database.comparison import gt

        self.assertFalse(gt({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertFalse(gt({u'S': u'waldo'}, {u'S': u'waldo1'}))
        self.assertTrue(gt({u'S': u'waldo'}, {u'S': u'wald'}))

        self.assertFalse(gt({u'N': u'42'}, {u'N': u'42'}))
        self.assertFalse(gt({u'N': u'42'}, {u'N': u'42.001'}))
        self.assertTrue(gt({u'N': u'42'}, {u'N': u'7'}))

    def test_begins_with(self):
        from ddbmock.database.comparison import begins_with

        self.assertTrue(begins_with({u'S': u'waldo'}, {u'S': u'waldo'}))
        self.assertTrue(begins_with({u'S': u'waldo'}, {u'S': u'wal'}))
        self.assertFalse(begins_with({u'S': u'waldo'}, {u'S': u'waldo-mario'}))

    def test_between(self):
        from ddbmock.database.comparison import between

        self.assertTrue(between({u'S': u'waldo'}, {u'S': u'wal-mart'}, {u'S': u'walee'}))
        self.assertFalse(between({u'S': u'waldo'}, {u'S': u'wale'}, {u'S': u'walee'}))
        self.assertTrue(between({u'N': u'42'}, {u'N': u'7'}, {u'N': u'123'}))
        self.assertTrue(between({u'N': u'42'}, {u'N': u'42'}, {u'N': u'42'}))
        self.assertFalse(between({u'N': u'42'}, {u'N': u'43'}, {u'N': u'123'}))