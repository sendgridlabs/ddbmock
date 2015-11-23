# -*- coding: utf-8 -*-

from .types import table_name, table_page, Required, READ_PERMISSION

post = {
    Required(u'ExclusiveStartTableName', None): table_name,
    Required(u'Limit', None): table_page,
}

permissions = READ_PERMISSION
