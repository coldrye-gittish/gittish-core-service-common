# TBD:LICENSE

from gittish.logging import LoggerBuilder


# TBD:DOCUMENT must be used first
def log_unary_unary(name):

  def decorator(func):

    def wrapper(self, request, context, *argv, **kw):

      logger = LoggerBuilder.name(name).trail(request.trail).trace().build()
      logger.request(request)

      # pass logger to service method
      kw.update({'logger': logger})
      response = func.__call__(request, context, *argv, **kw)
      logger.response(response)
      logger.pop_trace()

      return response

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__

    return wrapper

  return decorator


# TBD:DOCUMENT must be used first
def log_unary_stream(name):

  def decorator(func):

    def wrapper(self, request, context, *argv, **kw):

      logger = LoggerBuilder.name(name).trail(request.trail).trace().build()
      logger.request(request)

      #logger.set_trail(request.trail)
      #logger.push_trace(logger.generate_trace_id())

      # pass logger to service method
      kw.update({'logger': logger})
      response_iter = func.__call__(request, context, *argv, **kw)

      for response in logger.response_stream(response_iter):
        yield response

      logger.pop_trace()

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__

    return wrapper

  return decorator


# TBD:DOCUMENT must be used first
def log_stream_unary(name):

  def decorator(func):

    def wrapper(self, request_iter, context, *argv, **kw):

      logger = LoggerBuilder.name(name).stream_trail().trace().build()

      # pass logger to service method
      kw.update({'logger': logger})
      response = func.__call__(iter(logger.request_stream(request_iter)), context, *argv, **kw)

      logger.log_response(result)

      logger.pop_trace()

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__

    return wrapper

  return decorator


# TBD:DOCUMENT must be used first
def log_stream_stream(name):

  def decorator(func):

    def wrapper(self, request_iter, context, *argv, **kw):

      logger = LoggerBuilder.name(name).stream_trail().trace().build()

      # pass logger to service method
      kw.update({'logger': logger})
      response_iter = func.__call__(iter(logger.request_stream(request_iter)), context, *argv, **kw)

      for response in iter(logger.response_stream(response_iter))
        yield response

      logger.pop_trace()

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__

    return wrapper

  return decorator

# vim: expandtab:ts=2:sw=2:
