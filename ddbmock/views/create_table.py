# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceInUseException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def create_table(post):
    table = DynamoDB().create_table(post[u'TableName'], post)

    if table is None:
        raise ResourceInUseException("Table {} already exists".format(post[u'TableName']))

    #FIXME: status should be "CREATING"
    return {
        "TableDescription": table.to_dict()
    }

# Pyramid route wrapper
@view_config(route_name='create_table', renderer='json')
def pyramid_create_table(request):
    return create_table(request.json)
