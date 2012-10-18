# -*- coding: utf-8 -*-

from ddbmock.utils import load_table
from ddbmock.errors import ValidationException

@load_table
def scan(post, table):
    #FIXME: this line is a temp workaround
    if u'ScanFilter' not in post:
        post[u'ScanFilter'] = {}
    if u'AttributesToGet' not in post:
        post[u'AttributesToGet'] = []
    if u'Count' not in post:
        post[u'Count'] = False
    if u'Limit' not in post:
        post[u'Limit'] = None
    if u'ExclusiveStartKey' not in post:
        post[u'ExclusiveStartKey'] = None

    if post[u'AttributesToGet'] and post[u'Count']:
        raise ValidationException("Can not filter fields when only count is requested")

    results = table.scan(
        post[u'ScanFilter'],
        post[u'AttributesToGet'],
        post[u'ExclusiveStartKey'],
        post[u'Limit'],
    )

    ret = {
        "Count": len(results.items),
        "ScannedCount": results.scanned,
        "ConsumedCapacityUnits": 0.5*results.size.as_units(),
        #TODO: last evaluated key where applicable
    }

    if not post[u'Count']:
        ret[u'Items'] = results.items

    return ret
