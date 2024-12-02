# -*- coding: utf-8 -*-
# """
# common_configs.py
# Created on Nov 29, 2024
# @ Author: Mazhar
# """

import logging
import os
import sys
from pathlib import Path
from types import FrameType
from typing import Any, List, cast

import yaml
from colorama import Fore, Style, init
from easydict import EasyDict
from loguru import logger

# from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

# Initialize colorama for colored logs
init(autoreset=True)

CONFIG_YML_PATH = "./configs/configs.yml"


# # Use an absolute path for CONFIG_YML_PATH
# CONFIG_YML_PATH = os.path.join(os.path.dirname(__file__))
# print(f"CONFIG_YML_PATH: {CONFIG_YML_PATH}")

# Load the YAML config file for logging
with open(CONFIG_YML_PATH, "r") as file:
    config: Any = yaml.safe_load(file)

# Access the logging variables from the YAML config
LOG_DIR: str = config["LOGGING"].get("LOG_DIR", None)


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are type int


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    BASE_URL: str
    MODEL_NAME: str
    EMBEDDING_MODEL: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8001",  # type: ignore
        "*",
    ]

    SERVERS: list[dict[str, str]] = [
        # For Production Deployment
        # {
        #     "url": "https://more-socially-fly.ngrok-free.app",
        #     "description": "NGROK server with HTTPS",
        # },
        # For Production Deployment
        {
            "url": "https://ai-cs-chatbot.onrender.com/",
            "description": "Render server with HTTPS",
        },
        {
            "url": "http://localhost:8001",
            "description": "Local server with HTTPS",
        },
    ]

    class Config:
        env_file: str = ".env"
        case_sensitive = True


# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level: str = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame: FrameType = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application."""

    log_dir: str = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)  # Create a log directory if it doesn't exist

    # Format for the log messages
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Configure Loguru logger
    logger.remove()  # Remove default logger
    logger.add(
        sys.stderr, level=config.logging.LOGGING_LEVEL, format=log_format
    )  # CLI sink
    logger.add(
        os.path.join(log_dir, "file_{time}.log"),
        rotation="100 KB",
        retention=1,
        level=config.logging.LOGGING_LEVEL,
        format=log_format,
    )  # File sink

    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger: logging = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # logger.configure(
    #     handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    # )


# settings = Settings()


# Function to load configuration from YAML file
def cfg_from_yaml_file(cfg_file) -> EasyDict:
    with open(cfg_file, "r") as f:
        try:
            new_config: Any = yaml.load(f, Loader=yaml.FullLoader)
        except:
            new_config: Any = yaml.load(f)

    cfg = EasyDict(new_config)

    # Get the root directory (api folder)
    cfg.ROOT_DIR = (Path(__file__).resolve().parent / "..").resolve()

    # Convert relative paths to absolute paths
    for key, path in cfg.PATHS.items():
        cfg.PATHS[key] = str(cfg.ROOT_DIR / path.lstrip("./"))

    return cfg


# Load the configuration once
_cfg: EasyDict = cfg_from_yaml_file(CONFIG_YML_PATH)


def get_config() -> EasyDict:
    """Return the loaded configuration."""
    return _cfg


# # Custom formatter to include colors in logs
# class ColoredFormatter(logging.Formatter):
#     def format(self, record) -> str:
#         # Add colors based on the log level
#         if record.levelno == logging.INFO:
#             record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
#         elif record.levelno == logging.DEBUG:
#             record.msg = f"{Fore.CYAN}{record.msg}{Style.RESET_ALL}"
#         elif record.levelno == logging.WARNING:
#             record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
#         elif record.levelno == logging.ERROR:
#             record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
#         elif record.levelno == logging.CRITICAL:
#             record.msg = f"{Fore.MAGENTA}{record.msg}{Style.RESET_ALL}"
#         return super().format(record)


# # Logging setup based on configs.yml
# def setup_logging(config_path=CONFIG_YML_PATH) -> logging.Logger:
#     # Load the YAML config file for logging
#     with open(config_path, "r") as file:
#         config: Any = yaml.safe_load(file)

#     # Access the logging variables from the YAML config
#     LOG_FILE: str = config["LOGGING"].get("LOG_FILE", None)
#     LOG_LEVEL: str = config["LOGGING"]["LOG_LEVEL"]
#     LOG_FORMAT: str = config["LOGGING"]["LOG_FORMAT"]

#     # Convert LOG_LEVEL to logging module constants
#     log_level: int = logging.INFO if LOG_LEVEL == "INFO" else logging.DEBUG

#     # Set up logging formatter and handler
#     formatter = ColoredFormatter(LOG_FORMAT)
#     handler: logging.Handler = logging.StreamHandler()
#     handler.setFormatter(formatter)

#     # Basic logging configuration with or without file logging
#     # To log to file, set/uncomment LOG_FILE in configs.yml
#     if LOG_FILE:
#         logging.basicConfig(
#             level=log_level,
#             handlers=[handler, logging.FileHandler(LOG_FILE)],
#         )
#     else:
#         logging.basicConfig(
#             level=log_level,
#             handlers=[handler],
#         )

#     # Create and configure the logger object
#     logger: logging.Logger = logging.getLogger()

#     # Ensure the logger is only configured once
#     if not logger.hasHandlers():
#         logger.addHandler(handler)

#     return logger


# # Function to get logger, this will be used throughout the project
# def get_logger(config_path=CONFIG_YML_PATH) -> logging.Logger:
#     return setup_logging(config_path)


# # Distributed PyTorch initialization
# def init_dist_pytorch(batch_size, local_rank, backend="nccl") -> tuple[Any, int]:
#     if mp.get_start_method(allow_none=True) is None:
#         mp.set_start_method("spawn")
#     num_gpus: int = torch.cuda.device_count()
#     torch.cuda.set_device(local_rank % num_gpus)
#     dist.init_process_group(backend=backend)
#     assert (
#         batch_size % num_gpus == 0
#     ), "Batch size should be matched with GPUS: (%d, %d)" % (batch_size, num_gpus)
#     batch_size_each_gpu: int = batch_size // num_gpus
#     rank: int = dist.get_rank()
#     return batch_size_each_gpu, rank


# # Get distributed information for PyTorch
# def get_dist_info() -> tuple[int, int]:
#     if torch.__version__ < "1.0":
#         initialized: bool = dist._initialized
#     else:
#         if dist.is_available():
#             initialized: bool = dist.is_initialized()
#         else:
#             initialized = False
#     if initialized:
#         rank: int = dist.get_rank()
#         world_size: int = dist.get_world_size()
#     else:
#         rank: int = 0
#         world_size: int = 1
#     return rank, world_size


# from common_config import get_logger

# logger = get_logger()

# logger.info("This is an info message.")
# logger.debug("This is a debug message.")
