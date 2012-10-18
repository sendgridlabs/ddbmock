# -*- coding: utf-8 -*-

from ddbmock.utils import load_table

@load_table
def update_table(post, table):
    table.update_throughput(post[u'ProvisionedThroughput'][u'ReadCapacityUnits'],
                            post[u'ProvisionedThroughput'][u'WriteCapacityUnits'],
                           )

    desc = table.to_dict()
    table.activate() # FIXME: This sould not be part of the view

    return {
        "TableDescription": desc,
    }
