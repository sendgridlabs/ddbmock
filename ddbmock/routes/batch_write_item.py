# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
@dynamodb_api_validate
def batch_write_item(post):
    #TODO: limit to 25/batch
    #TODO: unprocessed keys

    return {
        "Responses": DynamoDB().write_batch(post[u'RequestItems']),
    }
