# -*- coding: utf-8 -*-

from voluptuous import Schema, Invalid
from importlib import import_module
from ddbmock.errors import ValidationException

# Cool function that automatically find and applies a validator for the input
# Crash if no validator were found (early breakage detection)
# Unless otherwise specified, all attributes are required
def dynamodb_api_validate(api):
    def wrapped(post):
        name = api.__name__
        mod = import_module('.{}'.format(name), __name__)
        validate = Schema(getattr(mod, 'post'), required=True)
        try:
            validate(post)
        except Invalid as e:
            raise ValidationException(e.errors)
        return api(post)
    return wrapped