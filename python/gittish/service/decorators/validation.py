# TBD:LICENSE

from gittish.protocol.error_pb2 import Error
from gittish.protocol.reqres_pb2 import Reqres
from gittish.protocol.timing_info_pb2 import TimingInfo


# TBD:DOCUMENT must be used after logger and before timer
def validate_request_unary_unary(validator):

  def decorator(func):

    def wrapper(self, request, context, *argv, **kw):

      result = None

      validation_errors = validator.validate(request)
      if validation_errors:
        data = Error(code = Error.INVALID_REQUEST, detail = validation_errors)
        result = Reqres(type = Reqres.ERROR, data = data.pack())
      else:
        result = func.__call__(self, request, context, *argv, **kw)

      return result

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__

    return wrapper

  return decorator


# TBD:DOCUMENT must be used after logger and before timer
def validate_request_unary_stream(validator):

  def decorator(func):

    def wrapper(self, request, context, *argv, **kw):

      validation_errors = validator.validate(request)
      if validation_errors:

        def response_generator():
          data = Error(code = Error.INVALID_REQUEST, detail = validation_errors)
          yield Reqres(type = Reqres.ERROR, data = data.pack())

        result = response_generator()
      else:
        result = func.__call__(self, request, context, *argv, **kw)

      return result

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__

    return wrapper


# TBD:DOCUMENT must be used after logger and before timer
def validate_request_stream_unary(validator):

  def decorator(func):

    def wrapper(self, request_iter, context, *argv, **kw):

      error_queue = []

      try:

        request_stream = _request_stream(request_iter, error_queue)
        result = func.__call__(self, request_stream, context, *argv, **kw)

      except ex:
        if not error_queue:
          # service method failed because of some other reason, rethrow
          raise
      finally:
        if error_queue:
          # service method failed due to missing expected next request
          # and we kind of expect it to do so, so we will ignore the exception
          result = error_queue.pop()

      return result

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__

    return wrapper


# TBD:DOCUMENT must be used after logger and before timer
def validate_request_stream_stream(validator):

  def decorator(func):

    def wrapper(self, request_iter, context, *argv, **kw):

      error_queue = []

      def _response_stream(response_iter, error_queue):
        while True:
          if error_queue:
            result = error_queue.pop()
            yield result
            break
          else:
            try:
              result = response_iter.__next__()
              yield result
            except:
              break

      try:

        request_stream = _request_stream(request_iter, error_queue)
        response_iter = func.__call__(self, request_stream, context, *argv, **kw)

        result = _response_stream(response_iter, error_queue)
      except ex:
        if not error_queue:
          # service method failed because of some other reason, rethrow
          raise
      finally:
        if error_queue:
          # service method failed due to missing expected next request
          # and we kind of expect it to do so, so we will ignore the exception
          result = _response_stream(None, error_queue)

      return result

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__

    return wrapper


def _request_stream(request_iter, error_queue):
  for request in request_iter:
    validation_errors = validator.validate(request)
    if validation_errors:
      data = Error(code = Error.INVALID_REQUEST, detail = validation_errors)
      error_queue.push(Reqres(type = Reqres.ERROR, data = data.pack())
      break
    yield request


# vim: expandtab:ts=2:sw=2:
