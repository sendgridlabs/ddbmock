# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def describe_table(post):
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    return {
        "Table": table.to_dict()
    }
