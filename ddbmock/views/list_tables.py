# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@wrap_exceptions
def list_tables(post):
    return {
        'TableNames': DynamoDB().list_tables()
    }

# Pyramid route wrapper
@view_config(route_name='pyramid_list_tables', renderer='json')
def pyramid_list_tables(request):
    return list_tables(request.json)