# -*- coding: utf-8 -*-

# This module is not imported unless connect_boto is called thus making 'boto'
# an optional dependancy

# boto entry point: semantic name
from __future__ import absolute_import

import json, time, itertools, boto

from boto.exception import DynamoDBResponseError
from boto.dynamodb.exceptions import (DynamoDBValidationError as DDBValidationErr,
                                      DynamoDBConditionalCheckFailedError)
from ddbmock.router import router
from ddbmock.errors import ValidationException, ConditionalCheckFailedException, DDBError

# DDB to Boto exception
def _ddbmock_exception_to_boto_exception(err):
    if isinstance(err, ValidationException):
        return DDBValidationErr(err.status, err.status_str, err.to_dict())
    elif isinstance(err, ConditionalCheckFailedException):
        return DynamoDBConditionalCheckFailedError(err.status, err.status_str, err.to_dict())
    else:
        return DynamoDBResponseError(err.status, err.status_str, err.to_dict())

request_counter = itertools.count()

# Boto lib version entry point
def boto_router(self, action, body='', object_hook=None):
    # from an external point of view, this function behaves exactly as the
    # original version. It only avoids all the HTTP and network overhead.
    # Even logs are preserved !
    # route to take is in 'action'
    # TODO:
    # - handle auth
    # - handle route errors (404)
    # - simulate retry/throughput errors ?
    target = '%s_%s.%s' % (self.ServiceName, self.Version, action)
    start = time.time()
    request_id = request_counter.next()

    boto.log.info("ddbmock: '%s' request (%s) => %s", action, request_id, body)

    try:
        ret = router(action, json.loads(body))
    except DDBError as e:
        raise _ddbmock_exception_to_boto_exception(e)
    finally:
        elapsed = (time.time() - start) * 1000
        boto.log.debug('RequestId: %s', request_id)
        boto.perflog.info('dynamodb %s: id=%s time=%sms',
                          target, request_id, int(elapsed))

    # Not in the finally block because, in case of error, they are already translated
    boto.log.info("ddbmock: '%s' answer (%s) => %s", action, request_id, ret)
    # FIXME: dump followed by load... can be better...
    ret = json.dumps(ret)
    return json.loads(ret, object_hook=object_hook)
