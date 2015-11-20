import json
import unittest
import helpers
from nose_parameterized import parameterized

class TestAuthUsers(unittest.TestCase):
    def setUp(self):
        from ddbmock.database.db import dynamodb
        from ddbmock.database.table import Table
        from ddbmock.database.key import PrimaryKey

        dynamodb.hard_reset()

    def tearDown(self):
        from ddbmock.database.db import dynamodb
        dynamodb.hard_reset()

    def test_invalid_user(self):
        self.app = helpers.makeTestApp(user = "invalid_user")
        from ddbmock import connect_boto_patch
        connect_boto_patch()

        expected = {
            u'message': u"Can't find invalid_user in users",
            u'__type': u'com.amazonaws.dynamodb.v20111205#AccessDeniedException'
        }

        res = self.app.post_json('/', {}, headers={}, status=400)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])

    def test_readonly_user_can_list(self):
        self.app = helpers.makeTestApp(user = "read_only")
        from ddbmock import connect_boto_patch
        connect_boto_patch()
        expected = {
            "TableNames": [],
        }
        request = {}

        HEADERS = {
            'x-amz-target': 'dynamodb_20111205.ListTables',
            'content-type': 'application/x-amz-json-1.0',
        }

        res = self.app.post_json('/', request, headers=HEADERS, status=200)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])

    @parameterized.expand([
        "create_table",
        "batch_write_item",
        "delete_item",
        "delete_table",
        "put_item",
        "update_item",
        "update_table"
    ], testcase_func_name=lambda funcname,_,param:"%s_%s" %( funcname.__name__, param[0][0]))
    def test_readonly_user_cant(self, name):
        self.app = helpers.makeTestApp(user = "read_only")
        from ddbmock import connect_boto_patch
        connect_boto_patch()
        expected = {
            u'message': u"User: read_only is not authorized to perform: dynamodb:%s on resource: *" % name,
            u'__type': u'com.amazonaws.dynamodb.v20111205#AccessDeniedException'
        }
        request = {}

        HEADERS = {
            'x-amz-target': 'dynamodb_20111205.%s' % name,
            'content-type': 'application/x-amz-json-1.0',
        }

        res = self.app.post_json('/', request, headers=HEADERS, status=400)
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])
