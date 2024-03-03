import time
import os
import datetime
import warnings
import logging
from logging.handlers import TimedRotatingFileHandler

from config import DEBUG, BASE_DATA_PATH, SESSION_KEY
from tools.file_manager import create_directory_structure

loggers = {}


def setup_logger(logger_name, path=None, allow_stream_log=False):
    log_dir_path = f"{BASE_DATA_PATH}/logs"
    if not os.path.isdir(log_dir_path):
        os.mkdir(log_dir_path)
        create_directory_structure(
            path=log_dir_path,
            strct={
                "operation": {},
                "training": {},
                "classification": {},
            }
        )

    if loggers.get(logger_name):
        return loggers.get(logger_name)
    else:

        custom_logger = logging.getLogger(f'senti_{logger_name}@{SESSION_KEY}')
        custom_handler = TimedRotatingFileHandler(
            f"{BASE_DATA_PATH}/logs/{logger_name}/{logger_name}.log",
            when='midnight', backupCount=5, interval=1
        )
        custom_handler.setLevel(logging.DEBUG)
        custom_handler.setFormatter(logging.Formatter(f'{SESSION_KEY} @&#&@ %(message)s;%(asctime)s'))
        custom_logger.addHandler(custom_handler)
        if allow_stream_log:
            stream_handler = logging.StreamHandler()
            custom_logger.addHandler(stream_handler)

        loggers[logger_name] = custom_logger
        return custom_logger


