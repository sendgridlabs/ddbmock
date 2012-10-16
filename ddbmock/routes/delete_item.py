# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

@wrap_exceptions
@dynamodb_api_validate
def delete_item(post):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    name = post[u'TableName']
    table = DynamoDB().get_table(name)
    item = table.delete_item(post[u'Key'], post[u'Expected'])

    ret = {
        "ConsumedCapacityUnits": item.get_size().as_units(),
        "Attributes": item,
    }

    if post[u'ReturnValues'] == "ALL_OLD":
        return ret
    else:
        del ret["Attributes"]
        return ret
