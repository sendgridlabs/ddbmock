# -*- coding: utf-8 -*-

from ddbmock.database import DynamoDB
from ddbmock.errors import wrap_exceptions

@wrap_exceptions
def create_table(post):
    table = DynamoDB().create_table(post[u'TableName'], post)

    desc = table.to_dict(verbose=False)
    table.activate() # FIXME: This sould not be patr of the view

    return {
        "TableDescription": desc,
    }
