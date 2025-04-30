"""
Copyright (c) Cutleast
"""

from typing import Annotated, override

from pydantic import Field

from core.utilities.logger import Logger

from .base_config import BaseConfig


class AppConfig(BaseConfig):
    """
    Class for managing application settings.
    """

    log_level: Annotated[Logger.Level, Field(alias="log.level")] = Logger.Level.DEBUG
    """Log level"""

    log_num_of_files: Annotated[int, Field(alias="log.num_of_files", ge=-1)] = 5
    """Number of newest log files to keep"""

    log_format: Annotated[str, Field(alias="log.format")] = (
        "[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s.%(funcName)s]: %(message)s"
    )
    """Log format"""

    log_date_format: Annotated[str, Field(alias="log.date_format")] = (
        "%d.%m.%Y %H:%M:%S"
    )
    """Log date format"""

    log_file_name: Annotated[str, Field(alias="log.file_name")] = (
        "%d-%m-%Y-%H-%M-%S.log"
    )
    """Log file name"""

    @override
    @staticmethod
    def get_config_name() -> str:
        return "app.json"
