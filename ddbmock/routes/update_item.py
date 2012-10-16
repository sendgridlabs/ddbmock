# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.validators import dynamodb_api_validate
from ddbmock.errors import wrap_exceptions, ResourceNotFoundException

@wrap_exceptions
@dynamodb_api_validate
def update_item(post):
    #FIXME: this line is a temp workaround
    if u'ReturnValues' not in post:
        post[u'ReturnValues'] = u"NONE"
    if u'Expected' not in post:
        post[u'Expected'] = {}

    name = post[u'TableName']
    table = DynamoDB().get_table(name)

    old, new = table.update_item(
            post[u'Key'],
            post[u'AttributeUpdates'],
            post[u'Expected'],
    )

    units = max(old.get_size().as_units(), new.get_size().as_units())
    ret = {"ConsumedCapacityUnits": units}

    if post[u'ReturnValues'] == "ALL_OLD":
        ret["Attributes"] = old
    elif post[u'ReturnValues'] == "ALL_NEW":
        ret["Attributes"] = new
    elif post[u'ReturnValues'] == "UPDATED_OLD":
        ret["Attributes"] = old - new
    elif post[u'ReturnValues'] == "UPDATED_NEW":
        ret["Attributes"] = new - old

    return ret
