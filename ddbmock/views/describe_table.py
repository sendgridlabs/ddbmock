from pyramid.view import view_config
from ddbmock.database import DynamoDB, PrimaryKey
from ddbmock.errors import *


@view_config(route_name='describe_table', renderer='json')
@WrapExceptions
def create_table(request):
    post = request.json

    if u'TableName' not in post:
        raise TypeError("No table name supplied")

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    if table is None:
        raise TypeError("Table {} does not exist".format(name))

    return {
        "Table": table.to_dict()
    }