# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

# Real work
@wrap_exceptions
@dynamodb_api_validate
def delete_table(post):
    name = post[u'TableName']
    ret = DynamoDB().delete_table(name)

    return {
        'TableDescription': ret,
    }

# Pyramid route wrapper
@view_config(route_name='delete_table', renderer='json')
def pyramid_delete_table(request):
    return delete_table(request.json)
