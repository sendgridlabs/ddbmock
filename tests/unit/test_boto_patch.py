# -*- coding: utf-8 -*-

import unittest, mock

ACTION = "CreateTable"
ACTION_404 = "!~I bet this route won't ever exist~!"
ROUTE = "create_table"
POST = {"toto":"titi"}

class TestBotoPatch(unittest.TestCase):
    @mock.patch("ddbmock.router.botopatch.import_module")
    def test_do_request_nominal(self, m_import):
        from ddbmock.router.botopatch import _do_request

        m_module = m_import.return_value
        m_route = m_module.create_table
        m_route.return_value = {}

        _do_request(ACTION, POST)

        m_import.assert_called_with("ddbmock.views.{}".format(ROUTE))
        m_route.assert_called_with(POST)

    @mock.patch("ddbmock.router.botopatch.import_module")
    def test_do_request_route_NYI(self, m_import):
        from ddbmock.router.botopatch import _do_request
        from boto.exception import DynamoDBResponseError

        m_import.side_effect = ImportError

        self.assertRaisesRegexp(DynamoDBResponseError,
                                'implemented',
                                _do_request,
                                ACTION, POST)

    @mock.patch("ddbmock.router.botopatch.import_module")
    def test_do_request_route_404(self, m_import):
        from ddbmock.router.botopatch import _do_request
        from boto.exception import DynamoDBResponseError

        self.assertRaisesRegexp(DynamoDBResponseError,
                                'exist',
                                _do_request,
                                ACTION_404, POST)
