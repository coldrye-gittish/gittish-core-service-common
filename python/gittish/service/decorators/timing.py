# TBD:LICENSE

from gittish.utils.timer import Timer
from gittish.protocol.timing_info_pb2 import TimingInfo


# TBD:DOCUMENT should be used last in order to measure only the service method and not the decorators
def time_unary_unary(func):

  def wrapper(*argv, **kw):

    timer = Timer()
    timer.start()
    response = func.__apply__(*argv, **kw)
    timer.stop()
    response.timing_info = TimingInfo(begin = timer.begin, end = timer.end)

    return response

  wrapper.__name__ = func.__name__
  wrapper.__dict__ = func.__dict__
  wrapper.__doc__ = func.__doc__

  return wrapper


# TBD:DOCUMENT should be used last in order to measure only the service method and not the decorators
def time_unary_stream(func):

  def wrapper(*argv, **kw):

    timer = Timer()
    timer.start()
    response_iter = func.__apply__(*argv, **kw)

    def response_handler(response, timer):
      timer.stop()
      response.timing_info = TimingInfo(begin = timer.begin, end = timer.end)
      timer.reset()
      timer.start()

    return timer.stream(response_iter, response_handler)

  wrapper.__name__ = func.__name__
  wrapper.__dict__ = func.__dict__
  wrapper.__doc__ = func.__doc__

  return wrapper


# TBD:DOCUMENT should be used last in order to measure only the service method and not the decorators
def time_stream_unary(func):

  def wrapper(*argv, **kw):

    timer = Timer()
    timer.start()
    response = func.__apply__(*argv, **kw)
    timer.stop()
    response.timing_info = TimingInfo(begin = timer.begin, end = timer.end)

    return response

  wrapper.__name__ = func.__name__
  wrapper.__dict__ = func.__dict__
  wrapper.__doc__ = func.__doc__

  return wrapper


# TBD:DOCUMENT should be used last in order to measure only the service method and not the decorators
def time_stream_stream(func):

  def wrapper(request_iter, *argv, **kw):

    timer = Timer()

    def request_handler(request, timer):
      timer.start()

    def response_handler(response, timer):
      timer.stop()
      response.timing_info = TimingInfo(begin = timer.begin, end = timer.end)
      timer.reset()

    response_iter = func.__apply__(timer.stream(request_iter, request_handler), *argv, **kw)

    return timer.stream(response_iter, response_handler)

  wrapper.__name__ = func.__name__
  wrapper.__dict__ = func.__dict__
  wrapper.__doc__ = func.__doc__

  return wrapper

# vim: expandtab:ts=2:sw=2:
