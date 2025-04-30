"""
Copyright (c) Cutleast

Tests the main application class.
"""

import json
import time
from argparse import Namespace
from pathlib import Path
from threading import Thread

import pytest
from base_test import BaseTest
from pyfakefs.fake_filesystem import FakeFilesystem

from app import App
from core.process_listener.process_listener import ProcessListener
from core.wallpaper_manager.wallpaper_manager import WallpaperManager
from tests.utils import Utils


class TestApp(BaseTest):
    """
    Tests `app.App`.
    """

    def test_app(
        self, test_fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Tests correct initialization and running of the application.
        """

        # given
        args = Namespace()
        args.index_path = str(self.setup_categories())
        running_processes: list[str] = ["test.executable"]
        set_wallpaper_calls: list[Path] = []

        # Patch ProcessListener.get_running_processes() to return a custom list
        monkeypatch.setattr(
            ProcessListener, "get_running_processes", lambda: running_processes
        )
        monkeypatch.setattr(
            WallpaperManager, "set_wallpaper", set_wallpaper_calls.append
        )

        # when
        app = App(args)

        # then
        assert app.index == {
            "test.executable": Path("test_data/Test Executable"),
            "test2.executable": Path("test_data/Test Executable 2"),
        }

        # when
        Utils.get_private_method(app.process_listener, TestApp.CHECK, lambda: None)()

        # then
        assert len(set_wallpaper_calls) == 1
        assert set_wallpaper_calls[-1].is_relative_to(app.index["test.executable"])
        assert set_wallpaper_calls[-1].suffix != ".svg"

        # when
        running_processes.append("test2.executable")
        Utils.get_private_method(app.process_listener, TestApp.CHECK, lambda: None)()

        # then
        assert len(set_wallpaper_calls) == 2
        assert set_wallpaper_calls[-1].is_relative_to(app.index["test2.executable"])

        monkeypatch.undo()

    def test_run(
        self, test_fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Tests the `App.run()` method.
        """

        # given
        args = Namespace()
        args.index_path = str(self.setup_categories())
        running_processes: list[str] = ["test.executable"]
        set_wallpaper_calls: list[Path] = []

        # Patch ProcessListener.get_running_processes() to return a custom list
        monkeypatch.setattr(
            ProcessListener, "get_running_processes", lambda: running_processes
        )
        monkeypatch.setattr(
            WallpaperManager,
            "set_wallpaper",
            lambda path: set_wallpaper_calls.append(path),
        )

        app = App(args)

        # when
        app_thread = Thread(target=lambda: app.exec(0.1))
        app_thread.start()

        try:
            # then
            assert app_thread.is_alive()
            time.sleep(0.1)
            assert len(set_wallpaper_calls) == 1
            assert set_wallpaper_calls[-1].is_relative_to(app.index["test.executable"])

            # when
            running_processes.append("test2.executable")
            time.sleep(0.1)

            # then
            assert len(set_wallpaper_calls) == 2
            assert set_wallpaper_calls[-1].is_relative_to(app.index["test2.executable"])

            # when
            running_processes.remove("test2.executable")
            time.sleep(0.1)

            # then
            assert len(set_wallpaper_calls) == 2

            # when
            running_processes.remove("test.executable")
            time.sleep(0.1)

            # then
            assert len(set_wallpaper_calls) == 2
        except:
            app.exit()
            app_thread.join()
            raise

        app.exit()
        app_thread.join()

        monkeypatch.undo()

    def setup_categories(self) -> Path:
        """
        Sets up categories with dummy data and an index.json file.

        Returns:
            Path: The path to the created index.json file.
        """

        raw_index_data: dict[str, str] = {
            "test.executable": r"test_data\Test Executable",
            "test2.executable": r"test_data\Test Executable 2",
        }

        index_path: Path = Path("test_data") / "index.json"
        index_path.parent.mkdir()
        index_path.write_text(json.dumps(raw_index_data))

        folder1 = Path("test_data/Test Executable")
        folder1.mkdir()

        for s in [".jpg", ".png", ".svg"]:
            (folder1 / f"test{s}").touch()

        folder2 = Path("test_data/Test Executable 2")
        folder2.mkdir()

        for s in [".bmp", ".gif"]:
            (folder2 / f"test{s}").touch()

        return index_path
