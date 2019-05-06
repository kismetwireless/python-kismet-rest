"""All logging happens via this interface."""
import logging
import os


class Logger(object):
    """All logging happens here."""

    def __init__(self):
        """If ${DEBUG} env var is set to "True", level will be set to debug."""
        self.logger = logging.getLogger(__name__)
        msg_format = "%(asctime)-15s %(levelname)s %(name)s %(message)s"
        logging.basicConfig(format=msg_format)
        if os.getenv("DEBUG", "") in ["True", "true"]:
            self.set_debug()
        else:
            self.set_info()

    def set_debug(self):
        """Set logging to debug."""
        self.logger.setLevel(logging.DEBUG)

    def set_info(self):
        """Set logging to info."""
        self.logger.setLevel(logging.INFO)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def warn(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
