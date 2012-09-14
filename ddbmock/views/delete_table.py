from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *


@view_config(route_name='delete_table', renderer='json')
@WrapExceptions
def delete_tables(request):
    post = request.json

    if u'TableName' not in post:
        raise TypeError("No table name supplied")

    name = post[u'TableName']
    ret = DynamoDB().delete_table(name)
    if ret is None:
        raise ResourceNotFoundException("Table {} does not exist".format(name))

    return {
        'TableDescription': ret,
    }
