from pyramid.view import view_config
from ddbmock.errors import DDBError


@view_config(context=DDBError, renderer='json')
def failed_validation(exc, request):
    request.response.status = exc.status

    return {
        "__type": "com.amazonaws.dynamodb.v20111205#{}".format(type(exc).__name__),
        "message": exc.args[0] if exc.args else "",
    }
