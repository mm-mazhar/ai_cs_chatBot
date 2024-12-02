# -*- coding: utf-8 -*-
# """
# __init__.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """


from logging import Logger

from easydict import EasyDict

from .common_configs import Settings, get_config, setup_app_logging  # get_logger,

# Expose the configuration and logger
cfg: EasyDict = get_config()  # Load the configuration
# logger: Logger = get_logger()  # Get the logger instance

settings = Settings()
setup_logging = setup_app_logging


# # Optionally, expose specific paths or constants
# MENU_ITEMS_PATH = cfg.PATHS.MENU_ITEMS
# APRIORI_RECOMMENDATIONS_PATH = cfg.PATHS.APRIORI_RECOMMENDATIONS
# POPULARITY_RECOMMENDATIONS_PATH = cfg.PATHS.POPULARITY_RECOMMENDATIONS
