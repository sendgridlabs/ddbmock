from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

@view_config(route_name='list_tables', renderer='json')
@WrapExceptions
def list_tables(request):
    return {
        'TableNames': DynamoDB().list_tables()
    }
