# custom_logger.py

import logging
import os
import sys

from system_settings import *


def get_custom_logger(log_name: str) -> logging.Logger:

    sys_settings: SystemSettings = SystemSettings()

    # create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    logging_file_path: str = rf'{sys_settings.logging_file_path}'
    logging_file_name: str = os.path.join(logging_file_path, rf'{get_current_date()}.log')

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(logging_file_name)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    f_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return(logger)


def get_current_date() -> str:
#   ** ************************************************************************************************************************************************************
#   **
#   ** ************************************************************************************************************************************************************
    current_date_YYYYMMDD: datetime = datetime.datetime.now()
    current_year: str  = current_date_YYYYMMDD.strftime("%Y")
    current_month: str = current_date_YYYYMMDD.strftime("%m")
    current_day: str   = current_date_YYYYMMDD.strftime("%d")
    current_date:str   = rf'{current_year}{current_month}{current_day}'

    return (current_date)