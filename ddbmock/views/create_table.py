from pyramid.view import view_config
from ddbmock.database import DynamoDB, PrimaryKey
from ddbmock.errors import *

@view_config(route_name='create_table', renderer='json')
@WrapExceptions
def create_table(request):
    post = request.json

    table = DynamoDB().create_table(post[u'TableName'], post)

    if table is None:
        raise ResourceInUseException("Table {} already exists".format(post[u'TableName']))

    #FIXME: statis should be "CREATING"
    return {
        "TableDescription": table.to_dict()
    }
