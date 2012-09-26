# -*- coding: utf-8 -*-

from .types import table_name, optional, get_key_schema, return_values, expected_schema

post = {
    u'TableName': table_name,
    u'Key': get_key_schema,
    optional(u'Expected'): expected_schema, # It is optional but with a def value
    optional(u'ReturnValues'): return_values, # It is optional but with a def value
}
