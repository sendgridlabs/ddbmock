import json
import unittest
import helpers
from nose_parameterized import parameterized
from time import time

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

    @parameterized.expand([
        "batch_get_item",
        "describe_table",
        "get_item",
        "list_tables",
        "query",
        "scan"
    ], testcase_func_name=lambda funcname,_,param:"%s_%s" %( funcname.__name__, param[0][0]))
    def test_readonly_user_can(self, name):
        self.app = helpers.makeTestApp(user = "read_only")
        from ddbmock import connect_boto_patch
        connect_boto_patch()
        HEADERS = {
            'x-amz-target': 'dynamodb_20111205.%s'% name,
            'content-type': 'application/x-amz-json-1.0',
        }

        res = self.app.post_json('/', {}, headers=HEADERS, status=[200,400])
        ret = json.loads(res.body)
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8', res.headers['Content-Type'])

        # Because no arguments, we either get a 200 for things that require no args, or a 400 for things that need args
        if res.status_code == 200:
            return
        self.assertIn("__type", ret)
        self.assertEqual(u'com.amazonaws.dynamodb.v20111205#ValidationException', ret["__type"])

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

    def test_slow_user_is_slow(self):
        self.app = helpers.makeTestApp(user = "slow_user")
        from ddbmock import connect_boto_patch, config
        delay = 1
        config.config["slow_user"]["DELAY_OPERATIONS"] = delay
        connect_boto_patch()
        expected = {
            u'TableNames': []
        }
        request = {}

        HEADERS = {
            'x-amz-target': 'dynamodb_20111205.list_tables',
            'content-type': 'application/x-amz-json-1.0',
        }

        start = time()
        res = self.app.post_json('/', request, headers=HEADERS, status=200)
        end = time()
        self.assertEqual(expected, json.loads(res.body))
        self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                         res.headers['Content-Type'])

        self.assertAlmostEqual(delay, end-start, delta = 0.1)

    def test_intermittent_failure(self):
        self.app = helpers.makeTestApp(user = "intermittent_failure")
        from ddbmock import connect_boto_patch, config
        connect_boto_patch()
        request = {}

        HEADERS = {
            'x-amz-target': 'dynamodb_20111205.list_tables',
            'content-type': 'application/x-amz-json-1.0',
        }

        for _ in range(3):
            expected = {
                u'TableNames': []
            }

            res = self.app.post_json('/', request, headers=HEADERS, status=200)
            self.assertEqual(expected, json.loads(res.body))
            self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                             res.headers['Content-Type'])

            expected = {
                u'message': u"The server encountered an internal error trying to fulfill the request",
                u'__type': u'com.amazonaws.dynamodb.v20111205#InternalServerError'
            }
            res = self.app.post_json('/', request, headers=HEADERS, status=500)
            self.assertEqual(expected, json.loads(res.body))
            self.assertEqual('application/x-amz-json-1.0; charset=UTF-8',
                             res.headers['Content-Type'])
