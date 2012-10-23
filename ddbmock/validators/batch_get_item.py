# -*- coding: utf-8 -*-

from .types import table_name, Required, get_key_schema, attributes_to_get_schema

post = {
    u"RequestItems": {
        table_name: {
            u"Keys": [get_key_schema],
            Required(u'AttributesToGet', []): attributes_to_get_schema,
        },
    },
}
