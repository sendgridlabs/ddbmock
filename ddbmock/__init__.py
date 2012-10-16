# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from ddbmock.router.pyramid import pyramid_router

# Pyramid entry point
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Insert router as '/' route. This is because all DDB URL are '/' (!)
    config.add_route('pyramid_router', '')
    config.add_view(pyramid_router, route_name='pyramid_router')

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
    from router.boto import boto_router
    Layer1.make_request = boto_router
    return boto.connect_dynamodb()

# Legacy / compatibility. Scheduled to removed in 0.4.0
connect_boto = connect_boto_patch
connect_ddbmock = connect_boto_network
