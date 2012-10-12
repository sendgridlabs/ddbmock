# -*- coding: utf-8 -*-

from .types import table_name, batch_write_request

post = {
    u"RequestItems": {
        table_name: batch_write_request,
    },
}
