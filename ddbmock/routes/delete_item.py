# -*- coding: utf-8 -*-

from ddbmock.utils import load_table

@load_table
def delete_item(post, table):
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
