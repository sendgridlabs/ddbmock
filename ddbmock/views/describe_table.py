# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def describe_table(post):
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    return {
        "Table": table.to_dict()
    }

# Pyramid route wrapper
@view_config(route_name='describe_table', renderer='json')
def pyramid_describe_table(request):
    return describe_table(request.json)
