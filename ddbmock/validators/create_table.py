# -*- coding: utf-8 -*-

from .types import table_name, key_schema, provisioned_throughtput

post = {
    u'TableName': table_name,
    u'KeySchema': key_schema,
    u'ProvisionedThroughput': provisioned_throughtput,
}
