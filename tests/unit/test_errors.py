# -*- coding: utf-8 -*-

import unittest, mock

ARGS = ["all the arguments"]

class TestErrors(unittest.TestCase):
    def test_wrap_exceptions_nominal(self):
        from ddbmock.errors import wrap_exceptions

        m_func = mock.Mock()
        wrap_exceptions(m_func)(*ARGS)
        m_func.assert_called_with(*ARGS)

    def test_wrap_exceptions_valtyp_error(self):
        from ddbmock.errors import wrap_exceptions
        from ddbmock.errors import ValidationException

        m_func = mock.Mock()
        m_func.side_effect = TypeError

        self.assertRaises(ValidationException,
                          wrap_exceptions(m_func),
                          *ARGS)

    def test_wrap_exceptions_key_error(self):
        from ddbmock.errors import wrap_exceptions
        from ddbmock.errors import InternalServerError

        m_func = mock.Mock()
        m_func.side_effect = KeyError

        self.assertRaises(InternalServerError,
                          wrap_exceptions(m_func),
                          *ARGS)
