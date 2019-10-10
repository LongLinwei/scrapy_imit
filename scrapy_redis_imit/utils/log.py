import sys
import logging
from scrapy_imit.config.setting import DEFAULT_LOG_FILENAME,DEFAULT_LOG_DATEFMT,DEFAULT_LOG_FMT,DEFAULT_LOG_LEVEL
class Logger:
    def __init__(self):
        self._logger=logging.getLogger()
        self.formatter=logging.Formatter(fmt=DEFAULT_LOG_FMT,datefmt=DEFAULT_LOG_DATEFMT)
        self._logger.addHandler(self._get_file_handler(DEFAULT_LOG_FILENAME))
        self._logger.addHandler(self._get_console_handler())
        self._logger.setLevel(DEFAULT_LOG_LEVEL)

    def _get_file_handler(self,filename):
        filehandler=logging.FileHandler(filename=filename,encoding='utf8')
        filehandler.setFormatter(self.formatter)
        return filehandler
    def _get_console_handler(self):
        cosole_handler=logging.StreamHandler(sys.stdout)
        cosole_handler.setFormatter(self.formatter)
        return cosole_handler

    @property
    def logger(self):
        return self._logger

logger=Logger().logger