# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

@wrap_exceptions
@dynamodb_api_validate
def describe_table(post):
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    return {
        "Table": table.to_dict()
    }
