# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def create_table(post):
    table = DynamoDB().create_table(post[u'TableName'], post)

    return {
        "TableDescription": table.to_dict(verbose=False),
    }
