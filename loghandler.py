import logging
from logging.handlers import RotatingFileHandler

class LogHandler:
    """
      Create Logger required for data and
      error logging
    """
    def __init__(self, debug, logpath):
        self.infologger = logging.getLogger("DATA")
        self.errorlogger = logging.getLogger("MAINTENANCE")

        handler = RotatingFileHandler(logpath, maxBytes=10000000, backupCount=10)
        handler.setLevel(debug)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.infologger.addHandler(handler)
        self.errorlogger.setLevel(debug)

        handler.setLevel(logging.INFO)
        self.errorlogger.addHandler(handler)
        self.infologger.setLevel(logging.INFO)
        
