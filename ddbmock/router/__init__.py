# -*- coding: utf-8 -*-

from importlib import import_module
from ddbmock.errors import InternalFailure

# src: dest
routes = {
    'BatchGetItem':   'batch_get_item',
    'BatchWriteItem': 'batch_write_item',
    'CreateTable':    'create_table',
    'DeleteItem':     'delete_item',
    'DeleteTable':    'delete_table',
    'DescribeTable':  'describe_table',
    'GetItem':        'get_item',
    'ListTables':     'list_tables',
    'PutItem':        'put_item',
    'Query':          'query',
    'Scan':           'scan',
    'UpdateItem':     'update_item',
    'UpdateTable':    'update_table',
}

def router(action, post):
    # handles the request and wrap exceptions
    # Fixme: theses wrappers makes it very hard to find the actual issue...
    try:
        target = routes[action]
        mod = import_module('ddbmock.routes.{}'.format(target))
        func = getattr(mod, target)
        return func(post)
    except KeyError:
        raise InternalFailure("Method: {} does not exist".format(action))
    except ImportError:
        raise InternalFailure("Method: {} not yet implemented".format(action))
