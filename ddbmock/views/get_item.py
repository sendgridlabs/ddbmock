# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

# Real work
@wrap_exceptions
@dynamodb_api_validate
def get_item(post):
    #FIXME: this line is a temp workaround
    if u'AttributesToGet' not in post:
        post[u'AttributesToGet'] = []
    if u'ConsistentRead' not in post:
        post[u'ConsistentRead'] = False

    base_capacity = 1 if post[u'ConsistentRead'] else 0.5
    table = DynamoDB().get_table(post[u'TableName'])
    item = table.get(post[u'Key'], post[u'AttributesToGet'])

    if item is not None:
        return {
            "ConsumedCapacityUnits": base_capacity*item.get_units(),
            "Item": item,
        }
    else:
        return {
            "ConsumedCapacityUnits": base_capacity,
        }

# Pyramid route wrapper
@view_config(route_name='get_item', renderer='json')
def pyramid_get_item(request):
    return get_item(request.json)
