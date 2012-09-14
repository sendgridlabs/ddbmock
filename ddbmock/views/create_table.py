from pyramid.view import view_config
from ddbmock.database import DynamoDB, PrimaryKey
from ddbmock.errors import *


def key_from_request(data):
    if u'AttributeName' not in data:
        raise TypeError("No attribute name")
    if u'AttributeType' not in data:
        raise TypeError("No attribute type")

    return PrimaryKey(data[u'AttributeName'], data[u'AttributeType'])

@view_config(route_name='create_table', renderer='json')
@WrapExceptions
def create_table(request):
    post = request.json

    if u'TableName' not in post:
        raise TypeError("No table name supplied")
    if u'ProvisionedThroughput' not in post:
        raise TypeError("No throughput provisioned")
    if u'KeySchema' not in post:
        raise TypeError("No schema")
    if u'WriteCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No WRITE throughput provisioned")
    if u'ReadCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No READ throughput provisioned")

    if u'HashKeyElement' not in post[u'KeySchema']:
        raise TypeError("No hash_key")
    if u'RangeKeyElement' in post[u'KeySchema']:
        range_key = key_from_request(post[u'KeySchema'][u'RangeKeyElement'])
    hash_key = key_from_request(post[u'KeySchema'][u'HashKeyElement'])

    table = DynamoDB().create_table(post[u'TableName'],
                                    post[u'ProvisionedThroughput'][u'ReadCapacityUnits'],
                                    post[u'ProvisionedThroughput'][u'WriteCapacityUnits'],
                                    hash_key,
                                    range_key,
                                    )

    if table is None:
        raise ResourceInUseException("Table {} already exists".format(post[u'TableName']))

    return {
        u"TableDescription":{
            u"CreationDateTime": 1.310506263362E9, # TODO STUB
            u"KeySchema": post[u'KeySchema'],
            u"ProvisionedThroughput": post[u'ProvisionedThroughput'],
            u"TableName": post[u'TableName'],
            u"TableStatus": u"CREATING" # Autre Stub
            }
        }
