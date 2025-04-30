"""
Copyright (c) Cutleast

Base class for all tests.
"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem


class BaseTest:
    """
    Base class for all tests.
    """

    CHECK: str = "check"
    """Identifier for accessing the private check method of ProcessListener."""

    @pytest.fixture
    def data_folder(self) -> Path:
        """
        Returns the path to the test data folder.

        Returns:
            Path: The path to the test data folder.
        """

        return Path("tests") / "data"

    @pytest.fixture
    def test_fs(self, data_folder: Path, fs: FakeFilesystem) -> FakeFilesystem:
        """
        Creates a fake filesystem for testing.

        Returns:
            FakeFilesystem: The fake filesystem.
        """

        # TODO: Check if still required
        if data_folder.is_dir():
            fs.add_real_directory(data_folder)

        return fs
