# -*- coding: utf-8 -*-

# Very bad import statement
from voluptuous import *
import re

# Elementary types

table_name = all(
    unicode,
    length(min=3, max=255, msg="Table name length must be between 3 and 255"),
    match(re.compile(r'^[a-zA-Z0-9\-_\.]*$'), msg="Table name may only containe alphanumeric chars and '-' '_' '.'"),
)

table_page = all(
    int,
    range(1, 100, msg="Table pages can only contain from 1 to 100 table"),
)

key_name = all(
    unicode,
    length(min=1, max=255, msg="Key lenght must be between 1 and 255"),
)

primary_key_type = all(
    unicode,
    any(u'S', u'N', u'B', msg="Primary key type may only be one of 'S', 'N' or 'B'"),
)

throughtput = all(
    int,
    range(1, 10000, msg="throughtput value must be between 1 and 10000"),
)

# complex types

provisioned_throughtput = {
    u'ReadCapacityUnits':  throughtput,
    u'WriteCapacityUnits': throughtput,
}

primary_key = {
    u'AttributeName': key_name,
    u'AttributeType': primary_key_type,
}

key_schema = {
    u'HashKeyElement': primary_key,
    optional(u'RangeKeyElement'): primary_key,
}