# -*- coding: utf-8 -*-

from importlib import import_module
from ddbmock.errors import InternalFailure, ValidationException
from ddbmock.validators import dynamodb_api_validate
import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def action_to_route(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

def router(action, post):
    # Find route
    try:
        target = action_to_route(action)
        mod = import_module('ddbmock.routes.{}'.format(target))
        func = getattr(mod, target)
    except ImportError:
        raise InternalFailure("Method: {} does not exist".format(action))

    # Validate the input
    dynamodb_api_validate(target, post)

    # Run request and translate engine errors to DynamoDB errors
    try:
        return func(post)
    except (TypeError, ValueError, KeyError) as e:
        raise ValidationException(*e.args)
