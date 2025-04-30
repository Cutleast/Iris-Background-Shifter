"""
Copyright (c) Cutleast

Class for managing a set of desktop wallpaper.
"""

import ctypes
import logging
import random
from pathlib import Path

from . import (
    SPI_SETDESKWALLPAPER,
    SPIF_UPDATEINIFILE,
    SUPPORTED_EXTS,
    ImageNotSupportedError,
    WallpaperChangeFailedError,
)


class WallpaperManager:
    """
    Class for managing a set of desktop wallpapers.
    """

    __image_index: dict[str, Path]
    """Map of category name and folders with image files."""

    log: logging.Logger = logging.getLogger("WallpaperManager")

    def __init__(self, image_index: dict[str, Path]) -> None:
        self.__image_index = image_index

    def get_random_image(self, category: str) -> Path:
        """
        Returns a random image from the specified category.

        Args:
            category (str): Name of the category

        Returns:
            Path: Path to the image

        Raises:
            KeyError: If the category does not exist
            FileNotFoundError: If the folder of the category does not exist
            ValueError: If the folder of the category does not contain any images
        """

        category_folder: Path = self.__image_index[category]

        if not category_folder.is_dir():
            raise FileNotFoundError(f"Folder '{category_folder}' does not exist!")

        images: list[Path] = [
            f for suffix in SUPPORTED_EXTS for f in category_folder.glob(f"*{suffix}")
        ]

        if len(images) == 0:
            raise ValueError(f"Folder '{category_folder}' does not contain any images!")

        return random.choice(images)

    @staticmethod
    def set_wallpaper(image_path: Path) -> None:
        """
        Sets the desktop wallpaper to the image at the specified path.

        Args:
            image_path (Path): Path to the image

        Raises:
            FileNotFoundError: If the image does not exist
            ImageNotSupportedError: If the image has an unsupported file extension
            WallpaperChangeFailed: If the wallpaper could not be changed
        """

        formatted_image_path: str = str(image_path.resolve()).replace("/", "\\")

        if not Path(formatted_image_path).is_file():
            raise FileNotFoundError(f"File '{formatted_image_path}' does not exist!")

        if Path(formatted_image_path).suffix.lower() not in SUPPORTED_EXTS:
            raise ImageNotSupportedError(
                f"File '{formatted_image_path}' has an unsupported file extension!"
            )

        WallpaperManager.log.info(f"Setting wallpaper to '{formatted_image_path}'...")

        ret_code: int = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, formatted_image_path, SPIF_UPDATEINIFILE
        )

        if ret_code == 0:
            raise WallpaperChangeFailedError(
                f"Function returned error code: {ret_code}"
            )

        WallpaperManager.log.info(f"Wallpaper set to '{formatted_image_path}'.")
