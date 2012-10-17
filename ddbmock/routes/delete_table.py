# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
def delete_table(post):
    name = post[u'TableName']
    ret = DynamoDB().delete_table(name)

    return {
        'TableDescription': ret,
    }
