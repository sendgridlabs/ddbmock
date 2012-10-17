# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def list_tables(post):
    return {
        'TableNames': DynamoDB().list_tables()
    }

