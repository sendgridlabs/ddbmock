# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def batch_get_item(post):
    #TODO: limit to 100/batch
    #TODO: unprocessed keys

    return {
        "Responses": DynamoDB().get_batch(post[u'RequestItems']),
    }

