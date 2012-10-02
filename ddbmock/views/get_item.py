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

    # hackish consistency
    capacity = 1 if post[u'ConsistentRead'] else 0.5

    #TODO: ConsistentRead
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    return {
        "ConsumedCapacityUnits": capacity, #FIXME: stub
        "Item": table.get(post[u'Key'], post[u'AttributesToGet']),
    }

# Pyramid route wrapper
@view_config(route_name='get_item', renderer='json')
def pyramid_get_item(request):
    return get_item(request.json)
