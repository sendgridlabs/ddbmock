# -*- coding: utf-8 -*-

from .types import table_name, optional, get_key_schema, return_values_all, expected_schema, attribute_update_schema

post = {
    u'TableName': table_name,
    u'Key': get_key_schema,
    u'AttributeUpdates': attribute_update_schema,
    optional(u'Expected'): expected_schema, # It is optional but with a def value
    optional(u'ReturnValues'): return_values_all, # It is optional but with a def value
}
