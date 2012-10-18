# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def delete_table(post):
    name = post[u'TableName']
    table = DynamoDB().delete_table(name)

    return {
        'TableDescription': table.to_dict(verbose=False)
    }
