# -*- coding: utf-8 -*-

from .types import table_name, provisioned_throughtput, WRITE_PERMISSION

post = {
    u'TableName': table_name,
    u'ProvisionedThroughput': provisioned_throughtput,
}

permissions = WRITE_PERMISSION
