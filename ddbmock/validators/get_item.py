# -*- coding: utf-8 -*-

from .types import table_name, Required, item_schema, consistent_read, attributes_to_get_schema, consumed_capacity, READ_PERMISSION

post = {
    u'TableName': table_name,
    u'Key': item_schema,
    u'ReturnConsumedCapacity': consumed_capacity,
    Required(u'AttributesToGet', []): attributes_to_get_schema,
    Required(u'ConsistentRead', False): consistent_read,
}

permissions = READ_PERMISSION
