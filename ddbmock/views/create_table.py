# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

# Real work
@wrap_exceptions
@dynamodb_api_validate
def create_table(post):
    table = DynamoDB().create_table(post[u'TableName'], post)

    desc = table.to_dict(verbose=False)
    table.activate() # FIXME: This sould not be patr of the view

    return {
        "TableDescription": desc,
    }

# Pyramid route wrapper
@view_config(route_name='create_table', renderer='json')
def pyramid_create_table(request):
    return create_table(request.json)
