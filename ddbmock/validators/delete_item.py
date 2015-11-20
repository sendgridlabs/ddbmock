# -*- coding: utf-8 -*-

from .types import table_name, Required, get_key_schema, return_values, expected_schema, WRITE_PERMISSION

post = {
    u'TableName': table_name,
    u'Key': get_key_schema,
    Required(u'Expected', {}): expected_schema,
    Required(u'ReturnValues', u'NONE'): return_values,
}

permissions = WRITE_PERMISSION
