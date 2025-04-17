import logging
import logging.handlers
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from app_constants.app_configurations import LOG

if not os.path.exists(LOG.LOG_BASE_PATH):
    os.makedirs(LOG.LOG_BASE_PATH)

logging.trace = logging.DEBUG - 5
logging.addLevelName(logging.DEBUG - 5, 'TRACE')


class SupportLensLogger(logging.getLoggerClass()):
    def __init__(self, name):
        super().__init__(name)

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.trace):
            self._log(logging.trace, msg, args, **kwargs)


def get_logger():
    """sets logger mechanism"""
    _logger = logging.getLogger("Metamanager-service")
    _logger.setLevel(LOG.LOG_LEVEL)

    if LOG.LOG_LEVEL == 'DEBUG' or LOG.LOG_LEVEL == 'TRACE':
        _formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - '
                                       '%(lineno)d - %(message)s')
    else:
        _formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if 'file' in LOG.LOG_HANDLERS:
        _file_handler = logging.FileHandler(LOG.FILE_NAME)
        _file_handler.setFormatter(_formatter)
        _logger.addHandler(_file_handler)

    if 'rotating' in LOG.LOG_HANDLERS:
        _rotating_file_handler = RotatingFileHandler(filename=LOG.FILE_NAME,
                                                     maxBytes=int(LOG.FILE_BACKUP_SIZE),
                                                     backupCount=int(LOG.FILE_BACKUP_COUNT))
        _rotating_file_handler.setFormatter(_formatter)
        _logger.addHandler(_rotating_file_handler)

    if 'console' in LOG.LOG_HANDLERS:
        _console_handler = StreamHandler(sys.stdout)
        _console_handler.setFormatter(_formatter)
        _logger.addHandler(_console_handler)

    return _logger


logger = get_logger()
