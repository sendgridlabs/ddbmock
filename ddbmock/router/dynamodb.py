# -*- coding: utf-8 -*-

def dynamodb_router_factory(handler, registry):
    # if timing support is enabled, return a wrapper
    def dynamodb_router(request):
        # route rewrite
        target = request.headers.get('x-amz-target')
        if target is not None:
            (version, route) = target.split('.', 2)
            request.path_info = u'/%s' % route
        # Content type rewrite
        if request.content_type == 'application/x-amz-json-1.0':
            request.content_type = 'application/json'
        # Work on it
        response = handler(request)
        # Content type rewrite 2
        if response.content_type == 'application/json':
            response.content_type = 'application/x-amz-json-1.0'
        return response
    return dynamodb_router