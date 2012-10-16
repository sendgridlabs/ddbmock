# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
@dynamodb_api_validate
def batch_get_item(post):
    #TODO: limit to 100/batch
    #TODO: unprocessed keys

    return {
        "Responses": DynamoDB().get_batch(post[u'RequestItems']),
    }

