# -*- coding: utf-8 -*-

from voluptuous import Schema
from importlib import import_module

# Cool function that automatically find and applies a validator for the input
# Crash if no validator were found (early breakage detection)
# Unless otherwise specified, all attributes are required
def dynamodb_api_validate(api):
    def wrapped(post):
        #import ipdb; ipdb.set_trace()
        name = api.__name__
        mod = import_module('.{}'.format(name), __name__)
        validate = Schema(getattr(mod, 'post'), required=True)
        validate(post)
        return api(post)
    return wrapped