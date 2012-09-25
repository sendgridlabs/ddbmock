# -*- coding: utf-8 -*-

# This module is not imported unless connect_boto is called thus making 'boto'
# an optional dependancy

import json, time
import boto

from importlib import import_module
from boto.exception import DynamoDBResponseError
from boto.dynamodb.exceptions import DynamoDBValidationError as DDBValidationErr
from ddbmock.router import routes
from ddbmock.errors import *

# DDB to Boto exception
def _do_exception(err):
    if isinstance(err, ValidationException):
        raise DDBValidationErr(err.status, err.status_str, err.to_dict())
    else:
        raise DynamoDBResponseError(err.status, err.status_str, err.to_dict())

# Wrap the request logic
def _do_request(action, post):
    # handles the request and wrap exceptions
    # Fixme: theses wrappers makes it very hard to find the actual issue...
    try:
        target = routes[action]
        mod = import_module('ddbmock.views.{}'.format(target))
        func = getattr(mod, target)
        return json.dumps(func(post))
    except KeyError:
        err = InternalFailure("Method: {} does not exist".format(action))
    except ImportError:
        err = InternalFailure("Method: {} not yet implemented".format(action))
    except DDBError as e:
        err = e

    return _do_exception(err)

# Boto lib version entry point
def boto_make_request(self, action, body='', object_hook=None):
    # from an external point of view, this function behaves exactly as the
    # original version. It only avoids all the HTTP and network overhead.
    # Even logs are preserved !
    # route to take is in 'action'
    # TODO:
    # - handle auth
    # - handle route errors (404)
    # - handle all exceptions
    # - request ID
    # - simulate retry/throughput errors ?
    # FIXME: dump followed by load... can be better...
    target = '%s_%s.%s' % (self.ServiceName, self.Version, action)
    start = time.time()

    try:
        ret = _do_request(action, json.loads(body))
    except DDBError as e:
        raise
    finally:
        request_id = 'STUB'
        elapsed = (time.time() - start) * 1000
        boto.log.debug('RequestId: %s', request_id)
        boto.perflog.info('dynamodb %s: id=%s time=%sms',
                          target, request_id, int(elapsed))

    boto.log.debug(ret)
    return json.loads(ret, object_hook=object_hook)