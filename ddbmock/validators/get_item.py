# -*- coding: utf-8 -*-

from .types import table_name, optional, item_schema, get_key_schema, consistent_read, attributes_to_get_schema

post = {
    u'TableName': table_name,
    u'Key': get_key_schema,
    optional(u'AttributesToGet'): attributes_to_get_schema, #FIXME: handle default
    optional(u'ConsistentRead'): consistent_read,  #FIXME: handle default
}
