# -*- coding: utf-8 -*-

from importlib import import_module
from ddbmock.errors import InternalFailure
import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def action_to_route(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

def router(action, post):
    # handles the request and wrap exceptions
    # Fixme: theses wrappers makes it very hard to find the actual issue...
    try:
        target = action_to_route(action)
        mod = import_module('ddbmock.routes.{}'.format(target))
        func = getattr(mod, target)
        return func(post)
    except ImportError:
        raise InternalFailure("Method: {} does not exist".format(action))
