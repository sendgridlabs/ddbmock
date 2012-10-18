# -*- coding: utf-8 -*-

import unittest, mock

# tests
# - delete callback (known to be called but not to work :p)

TABLE_NAME = "tabloid"

class TestDB(unittest.TestCase):
    def setUp(self):
        from ddbmock.database import DynamoDB

        DynamoDB().data[TABLE_NAME] = mock.Mock()

    def test_internal_delet_table(self):
        from ddbmock.database import DynamoDB

        db = DynamoDB()

        # delete a table
        db._internal_delete_table(TABLE_NAME)
        self.assertNotIn(TABLE_NAME, db.data)

        # make sure deleting already deleted table does not harm
        db._internal_delete_table(TABLE_NAME)

    def test_delete_table(self):
        from ddbmock.database import DynamoDB

        db = DynamoDB()

        db.delete_table(TABLE_NAME)

        db.data[TABLE_NAME].delete.assert_called_withassert_called_with(callback=db._internal_delete_table)

