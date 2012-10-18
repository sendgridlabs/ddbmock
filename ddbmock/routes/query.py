# -*- coding: utf-8 -*-

from ddbmock.utils import load_table
from ddbmock.errors import ValidationException

@load_table
def query(post, table):
    #FIXME: this line is a temp workaround
    if u'RangeKeyCondition' not in post:
        post[u'RangeKeyCondition'] = None
    if u'AttributesToGet' not in post:
        post[u'AttributesToGet'] = []
    if u'Count' not in post:
        post[u'Count'] = False
    if u'Limit' not in post:
        post[u'Limit'] = None
    if u'ScanIndexForward' not in post:
        post[u'ScanIndexForward'] = True
    if u'ExclusiveStartKey' not in post:
        post[u'ExclusiveStartKey'] = None
    if u'ConsistentRead' not in post:
        post[u'ConsistentRead'] = False

    if post[u'AttributesToGet'] and post[u'Count']:
        raise ValidationException("Can filter fields when only count is requested")

    base_capacity = 1 if post[u'ConsistentRead'] else 0.5

    results = table.query(
        post[u'HashKeyValue'],
        post[u'RangeKeyCondition'],
        post[u'AttributesToGet'],
        post[u'ExclusiveStartKey'],
        not post[u'ScanIndexForward'],
        post[u'Limit'],
    )

    ret = {
        "Count": len(results.items),
        "ConsumedCapacityUnits": base_capacity*results.size.as_units(),
    }

    if results.last_key is not None:
        ret['LastEvaluatedKey'] = results.last_key

    if not post[u'Count']:
        ret[u'Items'] = results.items

    return ret
