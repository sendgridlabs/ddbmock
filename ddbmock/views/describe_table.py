# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@WrapExceptions
def _describe_table(post):
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
@view_config(route_name='describe_table', renderer='json')
def describe_table(request):
    return _describe_table(request.json)
