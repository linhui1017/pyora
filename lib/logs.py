import os
import sys
import logging
import time
from logging.handlers import TimedRotatingFileHandler
from settings import Config


def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path


DATEFMT = '%Y-%m-%d %H:%M:%S'
FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]", DATEFMT)
LOG_FILE = Config.LOG_URI 

# def get_console_handler():
#    console_handler = logging.StreamHandler(sys.stdout)
#    console_handler.setFormatter(FORMATTER)
#    return console_handler
# def get_file_handler():
#    file_handler = TimedRotatingFileHandler(LOG_FILE,when='H',interval=1,backupCount=745)
#    file_handler.setFormatter(FORMATTER)
#    return file_handler
# def get_logger(logger_name):
#    make_dir(Config.LOG_DIR) 
#    logger = logging.getLogger(logger_name)
#    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
#    logger.addHandler(get_console_handler())
#    logger.addHandler(get_file_handler())
#    # with this pattern, it's rarely necessary to propagate the error up to parent
#    logger.propagate = False
#    return logger

def initialize_log():
    make_dir(Config.LOG_DIR)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = TimedRotatingFileHandler(LOG_FILE,when='H',interval=2,backupCount=373)
    fh.setFormatter(FORMATTER)
    logger.addHandler(fh)

#     stdout_handler = logging.StreamHandler(sys.stdout)
#     stdout_handler.level = logging.DEBUG
#     stdout_handler.formatter = formatter
#     logger.addHandler(stdout_handler)
   
    # stderr_handler = logging.StreamHandler(sys.stderr)
    # stderr_handler.level = logging.WARNING
    # stderr_handler.formatter = FORMATTER
    # logger.addHandler(stderr_handler)
