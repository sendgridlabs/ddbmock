# -*- coding: utf-8 -*-

from ddbmock.utils import load_table

@load_table
def get_item(post, table):
    base_capacity = 1 if post[u'ConsistentRead'] else 0.5
    item = table.get(post[u'Key'], post[u'AttributesToGet'])

    if item is not None:
        return {
            "ConsumedCapacityUnits": base_capacity*item.get_size().as_units(),
            "Item": item,
        }
    else:
        return {
            "ConsumedCapacityUnits": base_capacity,
        }
