# -*- coding: utf-8 -*-

import unittest

HOST = 'samaritain'
PORT = -12321
ENDPOINT = '{}:{}'.format(HOST, PORT)

class TestDdbmockInit(unittest.TestCase):
    def test_connect_boto_patch_patch(self):
        from ddbmock import connect_boto_patch
        from ddbmock.router.boto import boto_router

        db = connect_boto_patch()

        self.assertEqual(boto_router, db.layer1.make_request.im_func)

    def test_connect_boto_patch_network(self):
        from ddbmock import connect_boto_network, clean_boto_patch

        # make sure no patch is active first
        clean_boto_patch()

        db = connect_boto_network(HOST, PORT)

        self.assertEqual('ddbmock', db.layer1.region.name)
        self.assertEqual(ENDPOINT, db.layer1.region.endpoint)
        self.assertEqual(ENDPOINT, db.layer1.host)
        self.assertEqual(PORT, db.layer1.port)
        self.assertFalse(db.layer1.is_secure)
