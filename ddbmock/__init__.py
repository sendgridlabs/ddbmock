import json, time
from ddbmock.errors import *
from pyramid.config import Configurator

# src: dest
routes = {
    'BatchGetItem':   'batch_get_item',
    'BatchWriteItem': 'batch_write_item',
    'CreateTable':    'batch_write_item',
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

# Pyramid entry point
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # Decipher DynamoDB routes

    config.add_tween('ddbmock.router.dynamodb.dynamodb_router_factory')
    # Add routes
    for src, dest in routes:
        config.add_route(dest, '/'.src)

    config.scan()
    return config.make_wsgi_app()

# Monkey patch magic, required for the Boto entry point
# Request hijacking Yeah !
def connect_boto():
    from boto.dynamodb.layer1 import Layer1
    Layer1.make_request = _boto_make_request

# Wrap the exception handling logic
def _do_request(action, post):
    try:
        target = routes[action]
        dest = __import__('ddbmock.views.{dest}._{dest}'.format(dest=target),
                        globals(), locals(), [], -1)
        return (200, json.dumps(dest(post)))
    except KeyError:
        err = InternalFailure("Method: {} does not exist".format(action))
    except ImportError:
        err = InternalFailure("Method: {} not yet implemented".format(action))
    except DDBError as e:
        err = e

    return (err.status, json.dumps(err.to_dict()))

# Boto lib version entry point
def _boto_make_request(self, action, body='', object_hook=None):
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
    import boto # do not make boto a global dependancy

    target = '%s_%s.%s' % (self.ServiceName, self.Version, action)
    start = time.time()
    (status, ret) = _do_request(action, json.loads(body))
    elapsed = (time.time() - start)*1000
    request_id = 'STUB'
    boto.log.debug('RequestId: %s' % request_id)
    boto.perflog.info('dynamodb %s: id=%s time=%sms',
                      target, request_id, int(elapsed))
    boto.log.debug(ret)
    return json.loads(ret, object_hook=object_hook)