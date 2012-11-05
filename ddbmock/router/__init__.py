# -*- coding: utf-8 -*-

from importlib import import_module
from ddbmock.errors import InternalFailure
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
        mod = import_module('ddbmock.operations.{}'.format(target))
        func = getattr(mod, target)
    except ImportError:
        raise InternalFailure("Method: {} does not exist".format(action))

    # Validate the input
    post = dynamodb_api_validate(target, post)

    # Run request and translate engine errors to DynamoDB errors
    try:
        return func(post)
    except (TypeError, ValueError, KeyError) as e:
        raise InternalFailure("{}: {}".format(type(e).__name__, str(e.args)))
