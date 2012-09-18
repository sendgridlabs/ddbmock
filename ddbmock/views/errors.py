# -*- coding: utf-8 -*-

from pyramid.view import view_config
from ddbmock.errors import DDBError

@view_config(context=DDBError, renderer='json')
def failed_validation(exc, request):
    request.response.status = exc.status
    return exc.to_dict()
