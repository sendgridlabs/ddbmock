# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@wrap_exceptions
def delete_table(post):
    if u'TableName' not in post:
        raise TypeError("No table name supplied")

    name = post[u'TableName']
    ret = DynamoDB().delete_table(name)
    if ret is None:
        raise ResourceNotFoundException("Table {} does not exist".format(name))

    return {
        'TableDescription': ret,
    }

# Pyramid route wrapper
@view_config(route_name='pyramid_delete_table', renderer='json')
def pyramid_delete_table(request):
    return delete_table(request.json)
