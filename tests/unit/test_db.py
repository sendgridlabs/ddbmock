# -*- coding: utf-8 -*-

import unittest, mock

# tests
# - delete callback (known to be called but not to work :p)

TABLE_NAME = "tabloid"

class TestDB(unittest.TestCase):
    def setUp(self):
        from ddbmock.database import dynamodb

        dynamodb.data[TABLE_NAME] = mock.Mock()

    def test_internal_delet_table(self):
        from ddbmock.database import dynamodb

        # delete a table
        dynamodb._internal_delete_table(TABLE_NAME)
        self.assertNotIn(TABLE_NAME, dynamodb.data)

        # make sure deleting already deleted table does not harm
        dynamodb._internal_delete_table(TABLE_NAME)

    def test_delete_table(self):
        from ddbmock.database import dynamodb

        dynamodb.delete_table(TABLE_NAME)
        dynamodb.data[TABLE_NAME].delete.assert_called_withassert_called_with(callback=dynamodb._internal_delete_table)

