# -*- coding: utf-8 -*-

from voluptuous import Schema, Invalid
from importlib import import_module
from ddbmock.errors import ValidationException

def dynamodb_api_validate(action, post):
    """ Find validator for ``action`` and run it on ``post``. If no validator
        are found, return False.

        :action: name of the route after translation to underscores
        :post: data to validate
        :return: False when no validator found, True on success
        :raises: any voluptuous exception
    """
    try:
        mod = import_module('.{}'.format(action), __name__)
        schema = getattr(mod, 'post')
    except (ImportError, AttributeError):
        return False # Fixme: should log

    try:
        validate = Schema(schema, required=True)
        validate(post)
    except Invalid as e:
        raise ValidationException(str(e.errors))

    return True
