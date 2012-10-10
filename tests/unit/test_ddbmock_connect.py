# -*- coding: utf-8 -*-

import unittest

HOST = 'samaritain'
PORT = -12321
ENDPOINT = '{}:{}'.format(HOST, PORT)

class TestDdbmockConnect(unittest.TestCase):
    def test_connect_boto_patch(self):
        from ddbmock import connect_boto_patch
        from ddbmock.router.botopatch import boto_make_request

        db = connect_boto_patch()

        self.assertEqual(boto_make_request, db.layer1.make_request.im_func)

    def test_connect_boto_network(self):
        from ddbmock import connect_boto_network

        db = connect_boto_network(HOST, PORT)

        self.assertEqual('ddbmock', db.layer1.region.name)
        self.assertEqual(ENDPOINT, db.layer1.region.endpoint)
        self.assertEqual(ENDPOINT, db.layer1.host)
        self.assertEqual(PORT, db.layer1.port)
        self.assertFalse(db.layer1.is_secure)

    def test_legacy(self):
        from ddbmock import (connect_boto_network, connect_boto_patch,
                             connect_boto, connect_ddbmock)

        self.assertEqual(connect_boto, connect_boto_patch)
        self.assertEqual(connect_ddbmock, connect_boto_network)


