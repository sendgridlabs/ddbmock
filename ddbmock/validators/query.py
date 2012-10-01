# -*- coding: utf-8 -*-

from .types import (
    table_name, optional, item_schema, consistent_read, limit, scan_index_forward,
    attributes_to_get_schema, key_field_value, range_key_condition, boolean,
    get_key_schema)

post = {
    u'TableName': table_name,
    u'HashKeyValue': key_field_value,
    optional(u'RangeKeyCondition'): range_key_condition,
    optional(u'ScanIndexForward'): boolean,
    optional(u'Count'): boolean,
    optional(u'Limit'): limit,
    optional(u'ExclusiveStartKey'): get_key_schema,
    optional(u'AttributesToGet'): attributes_to_get_schema, #FIXME: handle default
    optional(u'ConsistentRead'): consistent_read,  #FIXME: handle default
}
