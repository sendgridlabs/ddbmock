# -*- coding: utf-8 -*-

from .types import (
    table_name, optional, item_schema, consistent_read, limit, scan_filter,
    attributes_to_get_schema, key_field_value, boolean, get_key_schema)

post = {
    u'TableName': table_name,
    optional(u'ScanFilter'): scan_filter,
    optional(u'Count'): boolean,
    optional(u'Limit'): limit,
    optional(u'ExclusiveStartKey'): get_key_schema,
    optional(u'AttributesToGet'): attributes_to_get_schema, #FIXME: handle default
}
