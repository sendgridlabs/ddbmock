# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB

def put_item(post):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    name = post[u'TableName']
    table = DynamoDB().get_table(name)
    old, new = table.put(post[u'Item'], post[u'Expected'])
    units = max(old.get_size().as_units(), new.get_size().as_units())

    ret = {
        "ConsumedCapacityUnits": units,
    }

    if post[u'ReturnValues'] == "ALL_OLD":
        ret["Attributes"] = old

    return ret
