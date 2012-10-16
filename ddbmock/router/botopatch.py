# -*- coding: utf-8 -*-

# This module is not imported unless connect_boto is called thus making 'boto'
# an optional dependancy

import json, time, itertools
import boto

from importlib import import_module
from boto.exception import DynamoDBResponseError
from boto.dynamodb.exceptions import (DynamoDBValidationError as DDBValidationErr,
                                      DynamoDBConditionalCheckFailedError)
from ddbmock.router import routes
from ddbmock.errors import *

# DDB to Boto exception
def _ddbmock_exception_to_boto_exception(err):
    if isinstance(err, ValidationException):
        raise DDBValidationErr(err.status, err.status_str, err.to_dict())
    if isinstance(err, ConditionalCheckFailedException):
        raise DynamoDBConditionalCheckFailedError(err.status, err.status_str, err.to_dict())
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
        raise InternalFailure("Method: {} does not exist".format(action))
    except ImportError:
        raise InternalFailure("Method: {} not yet implemented".format(action))

request_counter = itertools.count()

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
    request_id = request_counter.next()

    boto.log.info("ddbmock: '%s' request (%s) => %s", action, request_id, body)

    try:
        ret = _do_request(action, json.loads(body))
    except Exception as e:
        _ddbmock_exception_to_boto_exception(e)
    finally:
        elapsed = (time.time() - start) * 1000
        boto.log.debug('RequestId: %s', request_id)
        boto.perflog.info('dynamodb %s: id=%s time=%sms',
                          target, request_id, int(elapsed))

    # Not in the finally block because, in case of error, they are already translated
    boto.log.info("ddbmock: '%s' answer (%s) => %s", action, request_id, ret)
    return json.loads(ret, object_hook=object_hook)
