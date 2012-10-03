# -*- coding: utf-8 -*-

from .types import table_name, optional, get_key_schema, attributes_to_get_schema

post = {
    u"RequestItems": {
        table_name: {
            u"Keys": [get_key_schema],
            optional(u'AttributesToGet'): attributes_to_get_schema, #FIXME: handle default,
        },
    },
}
