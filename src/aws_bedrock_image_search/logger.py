import logging
import os

from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

class Logger:
    """A universal logger class for all modules."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LOG_LEVEL)

        # Prevent duplicate handlers
        if not self.logger.hasHandlers():
            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
            self.logger.addHandler(console_handler)

            # File Handler with rotation
            file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=5)
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger

