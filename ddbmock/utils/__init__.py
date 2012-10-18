# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def load_table(func):
    def loader(post, *args):
        name = post[u'TableName']
        table = DynamoDB().get_table(name)

        return func(post, table, *args)
    return loader
