# -*- coding: utf-8 -*-

from ddbmock.utils import load_table

@load_table
def delete_item(post, table):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    item = table.delete_item(post[u'Key'], post[u'Expected'])

    if post[u'ReturnValues'] == "ALL_OLD":
        return {
            "ConsumedCapacityUnits": item.get_size().as_units(),
            "Attributes": item,
        }
    else:
        return {
            "ConsumedCapacityUnits": item.get_size().as_units(),
        }
