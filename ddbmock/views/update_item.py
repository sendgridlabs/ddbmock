# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def update_item(post):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    old, new = table.update_item(
            post[u'Key'],
            post[u'AttributeUpdates'],
            post[u'Expected'],
    )

    ret = {
        "ConsumedCapacityUnits": 1, #FIXME: stub
    }

    if post[u'ReturnValues'] == "ALL_OLD":
        ret["Attributes"] = old
    elif post[u'ReturnValues'] == "ALL_NEW":
        ret["Attributes"] = new
    elif post[u'ReturnValues'] == "UPDATED_OLD":
        ret["Attributes"] = old - new
    elif post[u'ReturnValues'] == "UPDATED_NEW":
        ret["Attributes"] = new - old

    return ret

# Pyramid route wrapper
@view_config(route_name='update_item', renderer='json')
def pyramid_update_item(request):
    return update_item(request.json)
