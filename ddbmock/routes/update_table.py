# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def update_table(post):
    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    table.update_throughput(post[u'ProvisionedThroughput'][u'ReadCapacityUnits'],
                            post[u'ProvisionedThroughput'][u'WriteCapacityUnits'],
                            )

    desc = table.to_dict()
    table.activate() # FIXME: This sould not be part of the view

    return {
        "TableDescription": desc,
    }
