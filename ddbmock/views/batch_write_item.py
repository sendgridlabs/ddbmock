# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

# Real work
@wrap_exceptions
@dynamodb_api_validate
def batch_write_item(post):
    #TODO: limit to 25/batch
    #TODO: unprocessed keys

    return {
        "Responses": DynamoDB().write_batch(post[u'RequestItems']),
    }

# Pyramid route wrapper
@view_config(route_name='batch_write_item', renderer='json')
def pyramid_batch_get_item(request):
    return batch_write_item(request.json)
