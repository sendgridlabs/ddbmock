# -*- coding: utf-8 -*-

from .types import table_name, Required, item_schema, consistent_read, attributes_to_get_schema

post = {
    u'TableName': table_name,
    u'Key': item_schema,
    Required(u'AttributesToGet', []): attributes_to_get_schema,
    Required(u'ConsistentRead', False): consistent_read,
}
