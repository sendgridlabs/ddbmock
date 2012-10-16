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
        from ddbmock.errors import InternalFailure

        m_import.side_effect = ImportError

        self.assertRaisesRegexp(InternalFailure,
                                'implemented',
                                _do_request,
                                ACTION, POST)

    @mock.patch("ddbmock.router.botopatch.import_module")
    def test_do_request_route_404(self, m_import):
        from ddbmock.router.botopatch import _do_request
        from ddbmock.errors import InternalFailure

        self.assertRaisesRegexp(InternalFailure,
                                'exist',
                                _do_request,
                                ACTION_404, POST)

    def test_routing_exception_transalation(self):
        from ddbmock.router.botopatch import _ddbmock_exception_to_boto_exception
        from boto.exception import DynamoDBResponseError
        from ddbmock.errors import InternalFailure

        self.assertRaisesRegexp(DynamoDBResponseError,
                                'taratata',
                                _ddbmock_exception_to_boto_exception,
                                InternalFailure('taratata'))

    def test_validation_exception_transalation(self):
        from ddbmock.router.botopatch import _ddbmock_exception_to_boto_exception
        from boto.dynamodb.exceptions import DynamoDBValidationError
        from ddbmock.errors import ValidationException

        self.assertRaisesRegexp(DynamoDBValidationError,
                                'taratata',
                                _ddbmock_exception_to_boto_exception,
                                ValidationException('taratata'))

    def test_conditions_exception_transalation(self):
        from ddbmock.router.botopatch import _ddbmock_exception_to_boto_exception
        from boto.dynamodb.exceptions import DynamoDBConditionalCheckFailedError
        from ddbmock.errors import ConditionalCheckFailedException

        self.assertRaisesRegexp(DynamoDBConditionalCheckFailedError,
                                'taratata',
                                _ddbmock_exception_to_boto_exception,
                                ConditionalCheckFailedException('taratata'))
