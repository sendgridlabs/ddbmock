# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException, ValidationException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def query(post):
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
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

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
        #TODO: last evaluated key where applicable
    }

    if not post[u'Count']:
        ret[u'Items'] = results.items

    return ret

# Pyramid route wrapper
@view_config(route_name='query', renderer='json')
def pyramid_query(request):
    return query(request.json)
