from pyramid.view import view_config
from ddbmock.database import DynamoDB, PrimaryKey
from ddbmock.errors import *

# Real work
@WrapExceptions
def _create_table(post):
    post = request.json

    table = DynamoDB().create_table(post[u'TableName'], post)

    if table is None:
        raise ResourceInUseException("Table {} already exists".format(post[u'TableName']))

    #FIXME: status should be "CREATING"
    return {
        "TableDescription": table.to_dict()
    }

# Pyramid route wrapper
@view_config(route_name='create_table', renderer='json')
def create_table(request):
    return _create_table(request.json)

