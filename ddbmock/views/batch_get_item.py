# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

# Real work
@wrap_exceptions
@dynamodb_api_validate
def batch_get_item(post):
    #TODO: limit to 100/batch
    #TODO: unprocessed keys

    return {
        "Responses": DynamoDB().get_batch(post[u'RequestItems']),
    }

# Pyramid route wrapper
@view_config(route_name='batch_get_item', renderer='json')
def pyramid_batch_get_item(request):
    return batch_get_item(request.json)
