# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
@dynamodb_api_validate
def list_tables(post):
    return {
        'TableNames': DynamoDB().list_tables()
    }

