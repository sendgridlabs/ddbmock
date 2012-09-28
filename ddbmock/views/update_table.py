# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

# Real work
@wrap_exceptions
@dynamodb_api_validate
def update_table(post):
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
@view_config(route_name='update_table', renderer='json')
def pyramid_update_table(request):
    return update_table(request.json)
