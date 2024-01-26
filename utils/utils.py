# utils.py

import logging

class ImmediateFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()  # Flush the stream after each log record is emitted

def setup_logging():
    logger = logging.getLogger('swarm_logger')
    logger.setLevel(logging.DEBUG)  # Set the log level

    if not logger.handlers:  # Only add handlers if they don't already exist
        # Create an immediate file handler
        file_handler = ImmediateFileHandler('logs\swarm.log')

        # Create console handler
        console_handler = logging.StreamHandler()

        # Set log format to include filename
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
