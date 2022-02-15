from logging import Logger
import logging
from .config import PROJECT_LOG_LEVEL, FORCE_MIN_LOG_LEVEL, FORCE_MAX_LOG_LEVEL

# logging.basicConfig(level=PROJECT_LOG_LEVEL)

# Just copy from log class not to import logging in addition to logger in project files.
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET
DEFAULT = NOTSET


def match_forced_levels(level):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            if level >= FORCE_MIN_LOG_LEVEL:
                if level >= FORCE_MAX_LOG_LEVEL:
                    args[0].logger.setLevel(DEBUG)
                    rv = fun(*args, **kwargs)
                    args[0].logger.setLevel(args[0].level)
                    return rv
                return fun(*args, **kwargs)
        return wrapper
    return decorator


class MeLogger:
    def __init__(self, level=DEFAULT, name='Me', traceback_level=ERROR):
        """
        logging encapsulation, allows to
        - easily set logging level for each class
        - use FORCE_MIN_LOG_LEVEL and FORCE_MAX_LOG_LEVEL
        - use the print function argument system in the log (meaning you don't need to follow the {".. %s", var} format
        :param level: logging level (PROJECT_LOG_LEVEL if notset)²
        :param name: name of the logger, default is the name of the project
        :param traceback_level: TODO
        """
        self._name = name
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s - %(asctime)s [%(name)s] %(message)s', datefmt='%y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.level = level
        self.logger.setLevel(level if level != DEFAULT else PROJECT_LOG_LEVEL)

    @staticmethod
    def merge(*args):
        return " ".join([str(i) for i in args])

    @match_forced_levels(INFO)
    def info(self, *args, **kwargs):
        self.logger.info(MeLogger.merge(*args), **kwargs)

    def i(self, *args, **kwargs):
        self.info(*args, **kwargs)

    @match_forced_levels(DEBUG)
    def debug(self, *args, **kwargs):
        # print("call debug with", self._name, MeLogger.merge(*args))
        self.logger.debug(MeLogger.merge(*args), **kwargs)

    def d(self, *args, **kwargs):
        self.debug(*args, **kwargs)

    @match_forced_levels(WARNING)
    def warn(self, *args, **kwargs):
        self.logger.warning(MeLogger.merge(*args), **kwargs)

    @match_forced_levels(ERROR)
    def error(self, *args, **kwargs):

        self.logger.error(MeLogger.merge(*args), **kwargs)

    def err(self, *args, **kwargs):
        self.error(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        default call is info
        """
        self.info(*args, **kwargs)

    def flush(self):
        for h in self.logger.handlers:
            h.flush()


def info(*args, **kwargs):
    logging.info(" ".join([str(i) for i in args]), kwargs)








