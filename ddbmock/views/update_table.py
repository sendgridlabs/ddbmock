# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@WrapExceptions
def _update_table(post):
    if u'TableName' not in post:
        raise TypeError("No table name supplied")
    if u'ProvisionedThroughput' not in post:
        raise TypeError("No throughput provisioned")
    if u'WriteCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No WRITE throughput provisioned")
    if u'ReadCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No READ throughput provisioned")


    table = DynamoDB().get_table(post[u'TableName'])
    if table is None:
        raise ResourceNotFoundException("Table {} does not exist".format(name))

    table.update_throughput(post[u'ProvisionedThroughput'][u'ReadCapacityUnits'],
                            post[u'ProvisionedThroughput'][u'WriteCapacityUnits'],
                            )

    #FIXME: status should be "UPDATING"
    return {
        "TableDescription": table.to_dict()
    }

# Pyramid route wrapper
@view_config(route_name='update_table', renderer='json')
def update_table(request):
    return _update_table(request.json)
