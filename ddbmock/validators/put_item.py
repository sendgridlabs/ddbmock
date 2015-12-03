# -*- coding: utf-8 -*-

from .types import table_name, Required, item_schema, return_values, expected_schema, WRITE_PERMISSION

post = {
    u'TableName': table_name,
    u'Item': item_schema,
    Required(u'Expected', {}): expected_schema, # It is optional but with a def value
    Required(u'ReturnValues', u'NONE'): return_values, # It is optional but with a def value
}

permissions = WRITE_PERMISSION
