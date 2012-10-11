# -*- coding: utf-8 -*-

# Very bad import statement
from voluptuous import *
from decimal import Decimal
import re

# backport, will be in following releases
def default_to(default_value, msg=None):
    def f(v):
        if v is None:
            # this is never executed because of conception error in voluptuous
            # but i keep it as a reminder
            v = default_value  # pragma: no coverage
        return v
    return f

# custom validator for integers
def precision(min=None, max=None, precision=None, msg=None):
    def f(v):
        d = Decimal(v)
        if precision is not None and len(d.as_tuple().digits) > precision:
            raise Invalid(msg or ('{} has {} digits but maximum is {}'.format(d, len(d.as_tuple().digits), precision)))
        if min is not None and min > d:
            raise Invalid(msg or ('{} is smaller than minimum {}'.format(d, min)))
        if max is not None and max < d:
            raise Invalid(msg or ('{} is bigger than maximum {}'.format(d, max)))
        return v
    return f

# Elementary types

base_64 = re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$')

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

return_values = all(
    default_to(u'NONE'),
    any(u'NONE', u'ALL_OLD', msg="If specified, return value may only be one of 'NONE' or 'ALL_OLD'"),
)

return_values_all = all(
    default_to(u'NONE'),
    any(u'NONE', u'ALL_OLD', u'UPDATED_OLD', u'ALL_NEW', u'UPDATED_NEW', msg="If specified, return value may only be one of 'ALL_OLD', 'UPDATED_OLD', 'ALL_NEW' or 'UPDATED_NEW'"),
)

consistent_read = all(
    default_to(False),
    boolean(msg="Consistent_read parameter must be a boolean"),
)

limit = all(
    int,
    range(min=1, msg="Limit parameter must be a positive integer"),
)

scan_index_forward = all(
    boolean(msg="ScanIndexForward must be either True either False"),
    default_to(True),
)

# DynamoDB data types

field_name = unicode

field_number_value = all(
    coerce(Decimal, msg="Number values shall be... numbers :)"),
    precision(min=Decimal('1E-128'), max=Decimal('1E+126'), precision=38),
)

field_string_value = all(unicode, length(min=1, msg="String fields can not be empty"))

field_binary_value = all(
    unicode,
    length(min=1, msg="Binary data fields can not be empty"),
    match(base_64, msg="Binary data must be base64 encoded"),

)

field_number_set_value = all(length(min=1, msg="A set can not be empty"), [field_number_value])
field_string_set_value = all(length(min=1, msg="A set can not be empty"), [field_string_value])
field_binary_set_value = all(length(min=1, msg="A set can not be empty"), [field_binary_value])

# complex types

provisioned_throughtput = {
    u'ReadCapacityUnits':  throughtput,
    u'WriteCapacityUnits': throughtput,
}

primary_key = {
    u'AttributeName': key_name,
    u'AttributeType': primary_key_type,
}

table_key_schema = {
    u'HashKeyElement': primary_key,
    optional(u'RangeKeyElement'): primary_key,
}

# Fixme: max 1 item
simple_field_value = {
    optional(u'N'): field_number_value,
    optional(u'S'): field_string_value,
    optional(u'B'): field_binary_value,
}

set_field_value = {
    optional(u'NS'): field_number_set_value,
    optional(u'SS'): field_string_set_value,
    optional(u'BS'): field_binary_set_value,
}

key_field_value = simple_field_value
field_value = simple_field_value.copy()
field_value.update(set_field_value)

single_str_num_bin_list = all(length(min=1, max=1), [simple_field_value])
single_str_bin_list = all(length(min=1, max=1), [{
    optional(u'S'): field_string_value,
    optional(u'B'): field_binary_value,
}])

item_schema = {
    required(field_name): field_value,
}

get_key_schema = {
    u'HashKeyElement': key_field_value,
    optional(u'RangeKeyElement'): key_field_value,
}

attributes_to_get_schema = all(
    default_to([]),
    [unicode],
)

expected_schema = {
    field_name: any(
        {"Exists": false},
        {"Exists": true, "Value": field_value}, # pas sur de la vraie syntaxe :/
        {"Value": field_value},
    )
}

# Tss, y'a pas idee de faire des API aussi tordu...
# catches only half of the validity conditions :/
update_action_schema = any(
    {"Value": field_value},  # FIXME: find a way to add "action=put" where nothing specified
    {"Value": field_value, "Action": "PUT"},
    {"Value": field_value, "Action": "ADD"},
    {"Value": set_field_value, "Action": "DELETE"},
    {"Action": "DELETE"},
)

attribute_update_schema = {
    field_name: update_action_schema
}

# Conditions shared by query and scan
range_key_condition = any(
    {
        u"ComparisonOperator": any(u"EQ", u"GT", u"GE", u"LT", u"LE", u"BETWEEN"),
        u"AttributeValueList": single_str_num_bin_list,
    },{
        u"ComparisonOperator": u"BEGINS_WITH",
        u"AttributeValueList": single_str_bin_list,
    },
)

# Conditions only implemented in scan
scan_condition = any(
    {
        u"ComparisonOperator": any(u"EQ", u"GT", u"GE", u"LT", u"LE", u"BETWEEN"),
        u"AttributeValueList": single_str_num_bin_list,
    },{
        u"ComparisonOperator": u"BEGINS_WITH",
        u"AttributeValueList": single_str_bin_list,
    },{
        u"ComparisonOperator": any(u"NULL", u"NOT_NULL"),
    },{
        u"ComparisonOperator": any(u"CONTAINS", u"NOT_CONTAINS"),
        u"AttributeValueList": single_str_num_bin_list,
    },{
        u"ComparisonOperator": u"IN",
        u"AttributeValueList": [simple_field_value],
    },
)

# Scan filter
scan_filter = {
    field_name: scan_condition,
}
