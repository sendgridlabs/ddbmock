class DDBError(Exception): pass

class BadRequest(DDBError): status=400
class ServerError(DDBError): status=500

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

def WrapExceptions(func):
    def wrapped(*args):
        try:
            return func(*args[1:])
        except (TypeError, ValueError) as e:
            raise ValidationException(*e.args)
    return wrapped
