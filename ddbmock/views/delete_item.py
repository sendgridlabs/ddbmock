# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def delete_item(post):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    ret = {
        "ConsumedCapacityUnits": 1, #FIXME: stub
        "Attributes": table.delete_item(post[u'Key'], post[u'Expected']),
    }

    if post[u'ReturnValues'] == "ALL_OLD":
        return ret
    else:
        del ret["Attributes"]
        return ret

# Pyramid route wrapper
@view_config(route_name='delete_item', renderer='json')
def pyramid_delete_item(request):
    return delete_item(request.json)
