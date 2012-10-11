# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

# tests
# - number validator

class TestValidators(unittest.TestCase):
    def test_number_max(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(3, precision(max=Decimal("3"))(3))
        self.assertRaisesRegexp(Invalid, "bigger",
                                precision(max=Decimal("3")),
                                3.1)

    def test_number_min(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(Decimal("-1.21E50"), precision(min=Decimal("-1.21E50"))(Decimal("-1.21E50")))
        self.assertRaisesRegexp(Invalid, "smaller",
                                precision(min=Decimal("-1.21E50")),
                                Decimal("-1.21001E50"))

    def test_number_precision(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(Decimal("-1.21E50"), precision(precision=3)(Decimal("-1.21E50")))
        self.assertRaisesRegexp(Invalid, "digits",
                                precision(precision=3),
                                Decimal("-1.211E50"))
