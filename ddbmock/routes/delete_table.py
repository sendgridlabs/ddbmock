# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
@dynamodb_api_validate
def delete_table(post):
    name = post[u'TableName']
    ret = DynamoDB().delete_table(name)

    return {
        'TableDescription': ret,
    }
