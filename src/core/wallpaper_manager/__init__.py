"""
Copyright (c) Cutleast
"""


class ImageNotSupportedError(ValueError):
    """
    Exception that is raised when an image is not supported because it has
    an unsupported file extension.
    """


class WallpaperChangeFailedError(OSError):
    """
    Exception that is raised when the wallpaper could not be changed.
    """


SUPPORTED_EXTS: set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

# Constants from https://stackoverflow.com/a/30018577
SPI_SETDESKWALLPAPER: int = 0x14  # which command (20)
SPIF_UPDATEINIFILE: int = 0x3  # forces instant update
