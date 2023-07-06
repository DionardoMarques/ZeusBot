import logging

def setupLogger(log_name, file_name, level=logging.INFO):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')

    specified_logger = logging.getLogger(log_name)

    # Check if a handler is already added to the logger
    if not specified_logger.handlers:
        handler = logging.FileHandler(file_name)
        handler.setFormatter(formatter)
        specified_logger.setLevel(level)
        specified_logger.addHandler(handler)

    return specified_logger