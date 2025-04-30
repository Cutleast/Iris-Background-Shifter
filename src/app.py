"""
Copyright (c) Cutleast

Main application class.
"""

import logging
import time
from argparse import Namespace
from pathlib import Path

import jstyleson as json

from core.config.app_config import AppConfig
from core.process_listener.process_listener import ProcessListener
from core.process_listener.process_state import ProcessState
from core.utilities.logger import Logger
from core.wallpaper_manager.wallpaper_manager import WallpaperManager


class App:
    """
    Main application class.
    """

    NAME: str = "Iris Background Shifter"
    VERSION: str = "development"
    AUTHOR: str = "Cutleast"

    args: Namespace
    config: AppConfig

    cur_path: Path = Path.cwd()
    data_path: Path = cur_path / "data"
    res_path: Path = cur_path / "res"
    config_path: Path = data_path / "config"
    log_path: Path = data_path / "logs"
    index_path: Path = data_path / "index.json"

    log: logging.Logger = logging.getLogger("App")
    logger: Logger

    index: dict[str, Path]
    wallpaper_manager: WallpaperManager
    process_listener: ProcessListener

    def __init__(self, args: Namespace) -> None:
        self.args = args

        if args.index_path:
            self.index_path = Path(args.index_path)
        elif not self.index_path.is_file():
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.index_path.write_text(r"{}", encoding="utf8")

        self.config = AppConfig.load(self.config_path)

        log_file: Path = self.log_path / time.strftime(self.config.log_file_name)
        self.logger = Logger(
            log_file, self.config.log_format, self.config.log_date_format
        )
        self.logger.setLevel(self.config.log_level)

        self.index = self.__load_index()

        self.__init_wallpaper_manager()
        self.__init_process_listener()

    def __load_index(self) -> dict[str, Path]:
        data: dict[str, str] = json.loads(self.index_path.read_text(encoding="utf8"))
        index: dict[str, Path] = {k: Path(v) for k, v in data.items()}

        self.log.info(f"Wallpaper index: {len(index)} categories")

        for cat_name, cat_path in index.items():
            self.log.info(
                f"{cat_name.rjust(max(len(name) for name in index) + 4)} = {cat_path}"
            )

        return index

    def __init_wallpaper_manager(self) -> None:
        self.wallpaper_manager = WallpaperManager(self.index)

    def __init_process_listener(self) -> None:
        self.process_listener = ProcessListener(
            list(self.index.keys()), [self.__on_process_change]
        )

    def __on_process_change(self, process_name: str, state: ProcessState) -> None:
        if state == ProcessState.Started:
            self.log.info(f"Changing wallpaper for started process '{process_name}'...")

            try:
                self.wallpaper_manager.set_wallpaper(
                    self.wallpaper_manager.get_random_image(process_name)
                )

            except Exception as ex:
                self.log.error(
                    f"Failed to change wallpaper for started process '{process_name}': {str(ex)}",
                    exc_info=ex,
                )

    def exec(self, check_interval: float = 10.0) -> None:
        """
        Executes the process listener.
        """

        try:
            self.process_listener.run(check_interval)
        except KeyboardInterrupt:
            pass

        self.clean()

        self.log.info("Exiting application...")

    def exit(self) -> None:
        """
        Stops the process listener and exits the application.
        """

        self.process_listener.stop()

    def clean(self) -> None:
        """
        Cleans up and exits application.
        """

        self.log.info("Cleaning...")

        # Clean up log files
        self.logger.clean_log_folder(
            self.log_path, self.config.log_file_name, self.config.log_num_of_files
        )
