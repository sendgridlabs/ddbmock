from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@WrapExceptions
def _list_tables(post):
    return {
        'TableNames': DynamoDB().list_tables()
    }

# Pyramid route wrapper
@view_config(route_name='list_tables', renderer='json')
def list_tables(request):
    return _list_tables(request.json)