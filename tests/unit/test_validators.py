# -*- coding: utf-8 -*-

import unittest
from decimal import Decimal

# tests
# - number validator

class TestValidators(unittest.TestCase):
    def test_number_max_exp(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(Decimal("382.1E4"), precision(max_exp=3)(Decimal("382.1E4")))
        self.assertRaisesRegexp(Invalid, "bigger",
                                precision(max_exp=3),
                                Decimal("395.1E5"))

    def test_number_min_exp(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(Decimal("-50.52"), precision(min_exp=-2)(Decimal("-50.52")))
        self.assertRaisesRegexp(Invalid, "smaller",
                                precision(min_exp=-2),
                                Decimal("-50.521"))

    def test_number_max_digits(self):
        from ddbmock.validators.types import precision
        from voluptuous import Invalid

        self.assertEqual(Decimal("-1.21E50"), precision(max_digits=3)(Decimal("-1.21E50")))
        self.assertRaisesRegexp(Invalid, "digits",
                                precision(max_digits=3),
                                Decimal("-1.211E50"))
