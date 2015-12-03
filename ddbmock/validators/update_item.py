# -*- coding: utf-8 -*-

from .types import (table_name, item_schema, return_values_all,
                    expected_schema, attribute_update_schema, Required, WRITE_PERMISSION)

post = {
    u'TableName': table_name,
    u'Key': item_schema,
    u'AttributeUpdates': attribute_update_schema,
    Required(u'Expected', {}): expected_schema,
    Required(u'ReturnValues', u'NONE'): return_values_all,
}

permissions = WRITE_PERMISSION
