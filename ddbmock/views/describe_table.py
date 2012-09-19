# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@wrap_exceptions
def describe_table(post):
    if u'TableName' not in post:
        raise TypeError("No table name supplied")

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    if table is None:
        raise TypeError("Table {} does not exist".format(name))

    return {
        "Table": table.to_dict()
    }

# Pyramid route wrapper
@view_config(route_name='pyramid_describe_table', renderer='json')
def pyramid_describe_table(request):
    return describe_table(request.json)
