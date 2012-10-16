# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException, ValidationException

@wrap_exceptions
@dynamodb_api_validate
def scan(post):
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

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

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
