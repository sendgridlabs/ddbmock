# -*- coding: utf-8 -*-

from voluptuous import optional
from .types import table_name, table_page

post = {
    optional(u'ExclusiveStartTableName'): table_name,
    optional(u'Limit'): table_page,
}