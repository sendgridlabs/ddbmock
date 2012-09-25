# -*- coding: utf-8 -*-

class DDBError(Exception):
    def to_dict(self):
        name = type(self).__name__
        msg = self.args[0] if self.args else ""

        return {
            "__type": "com.amazonaws.dynamodb.v20111205#{}".format(name),
            "message": msg,
        }

class BadRequest(DDBError):  status=400; status_str='Bad Request'
class ServerError(DDBError): status=500; status_str='InternalServerError'

class AccessDeniedException(BadRequest): pass
class ConditionalCheckFailedException(BadRequest): pass
class IncompleteSignatureException(BadRequest): pass
class LimitExceededException(BadRequest): pass
class MissingAuthenticationTokenException(BadRequest): pass
class ProvisionedThroughputExceededException(BadRequest): pass
class ResourceInUseException(BadRequest): pass
class ResourceNotFoundException(BadRequest): pass
class ThrottlingException(BadRequest): pass
class ValidationException(BadRequest): pass
class InternalFailure(ServerError): pass
class InternalServerError(ServerError): pass
class ServiceUnavailableException(ServerError): pass

def wrap_exceptions(func):
    def wrapped(*args):
        try:
            return func(*args)
        except (TypeError, ValueError) as e:
            raise ValidationException(*e.args)
        except KeyError as e:
            raise InternalServerError(*e.args)
    return wrapped
