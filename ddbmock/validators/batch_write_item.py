# -*- coding: utf-8 -*-

from .types import table_name, item_schema, Any, WRITE_PERMISSION

post = {
    u"RequestItems": {
        table_name: [Any(
            {
                u"PutRequest": {
                    u"Item": item_schema,
                }
            },{
                u"DeleteRequest": {
                    u"Key": item_schema,
                }
            },
        )],
    },
}

permissions = WRITE_PERMISSION
