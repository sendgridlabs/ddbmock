# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.errors import *

# Real work
@wrap_exceptions
def update_table(post):
    if u'TableName' not in post:
        raise TypeError("No table name supplied")
    if u'ProvisionedThroughput' not in post:
        raise TypeError("No throughput provisioned")
    if u'WriteCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No WRITE throughput provisioned")
    if u'ReadCapacityUnits' not in post[u'ProvisionedThroughput']:
        raise TypeError("No READ throughput provisioned")

    name = post[u'TableName']
    table = DynamoDB().get_table(name)
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
@view_config(route_name='pyramid_update_table', renderer='json')
def pyramid_update_table(request):
    return update_table(request.json)
