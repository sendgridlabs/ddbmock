# -*- coding: utf-8 -*-

import unittest, mock

ACTION = "CreateTable"
ACTION_404 = "!~I bet this route won't ever exist~!"
ROUTE = "create_table"
POST = {"toto":"titi"}

class TestRouterInit(unittest.TestCase):
    @mock.patch("ddbmock.router.import_module")
    def test_do_request_nominal(self, m_import):
        from ddbmock.router import router

        m_module = m_import.return_value
        m_route = m_module.create_table
        m_route.return_value = {}

        router(ACTION, POST)

        m_import.assert_called_with("ddbmock.routes.{}".format(ROUTE))
        m_route.assert_called_with(POST)

    @mock.patch("ddbmock.router.import_module")
    def test_do_request_route_NYI(self, m_import):
        from ddbmock.router import router
        from ddbmock.errors import InternalFailure

        m_import.side_effect = ImportError

        self.assertRaisesRegexp(InternalFailure,
                                'implemented',
                                router,
                                ACTION, POST)

    @mock.patch("ddbmock.router.import_module")
    def test_do_request_route_404(self, m_import):
        from ddbmock.router import router
        from ddbmock.errors import InternalFailure

        self.assertRaisesRegexp(InternalFailure,
                                'exist',
                                router,
                                ACTION_404, POST)
