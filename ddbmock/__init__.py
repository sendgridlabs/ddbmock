# -*- coding: utf-8 -*-

from ddbmock.router import routes
from pyramid.config import Configurator

# Pyramid entry point
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # Decipher DynamoDB routes

    config.add_tween('ddbmock.router.dynamodb.dynamodb_router_factory')
    # Add routes
    for src, dest in routes.iteritems():
        config.add_route(dest, '/{}'.format(src))

    config.scan()
    return config.make_wsgi_app()

# Regular "over the network" connection wrapper.
def connect_boto_network(host='localhost', port=6543):
    """Connect to ddbmock launched in *server* mode via boto"""
    import boto
    from boto.regioninfo import RegionInfo
    endpoint = '{}:{}'.format(host,port)
    region = RegionInfo(name='ddbmock', endpoint=endpoint)
    return boto.connect_dynamodb(region=region, port=port, is_secure=False)

# Monkey patch magic, required for the Boto entry point
# Request hijacking Yeah !
def connect_boto_patch():
    """Connect to ddbmock as a library via boto"""
    import boto
    from boto.dynamodb.layer1 import Layer1
    from router.botopatch import boto_make_request
    Layer1.make_request = boto_make_request
    return boto.connect_dynamodb()

# Legacy / compatibility. Scheduled to removed in 0.4.0
connect_boto = connect_boto_patch
connect_ddbmock = connect_boto_network
