"""Logging configuration for ari_backup package."""
import logging
import logging.handlers
import sys


class Logger(logging.Logger):
  """Subclass of the normal logger, to set up desired logging behavior.

  Specifically:
    ERROR and above go to stderr
    INFO and above go to syslog, unless debug is True then DEBUG and above
  """ 
  def __init__(self, name, debug=False, stderr_logging=True):
    """Initilizes Logger.

    Args:
      name: str, name passed to logging.Logger.
      debug: bool, whether to enable debug logging. Defaults to False.
      stderr_logging: bool, whether to log to stderr. Defaults to True.
    """
    logging.Logger.__init__(self, name)

    # Set the name, much like logging.getLogger(name) would.
    if debug:
      log_format = ('%(name)s [%(levelname)s] %(filename)s:%(lineno)d '
                    '%(message)s')
    else:
      log_format = '%(name)s [%(levelname)s] %(message)s'
    formatter = logging.Formatter(log_format)

    # Emit to sys.stderr, ERROR and above, unless debug is True.
    if stderr_logging:
      stream_handler = logging.StreamHandler(sys.stderr)
      if debug:
        stream_handler.setLevel(logging.DEBUG)
      else:
        stream_handler.setLevel(logging.ERROR)
      stream_handler.setFormatter(formatter)
      self.addHandler(stream_handler)

    # Emit to syslog, INFO and above, or DEBUG if debug.
    syslog_handler = logging.handlers.SysLogHandler('/dev/log')
    if debug:
        syslog_handler.setLevel(logging.DEBUG)
    else:
        syslog_handler.setLevel(logging.INFO)
    syslog_handler.setFormatter(formatter)
    self.addHandler(syslog_handler)
