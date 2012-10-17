# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
def list_tables(post):
    return {
        'TableNames': DynamoDB().list_tables()
    }

