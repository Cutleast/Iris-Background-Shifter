"""
Copyright (c) Cutleast

Script for building the application with nuitka.
"""

import logging
import re
import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any

project_file = Path("pyproject.toml")
project_data: dict[str, Any] = tomllib.loads(project_file.read_text(encoding="utf8"))[
    "project"
]
project_name: str = project_data["description"]
project_version: str = project_data["version"]
project_author: str = project_data["authors"][0]["name"]

VERSION_PATTERN: re.Pattern[str] = re.compile(r'(?<=VERSION: str = ")[^"]+(?=")')


logging.basicConfig(level=logging.DEBUG)


def prepare_src() -> None:
    logging.info(f"Preparing source code for '{project_name}'...")

    logging.debug("Copying source code to build directory...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.copytree("src", "build")

    # Set version string in app file
    logging.debug("Setting version string in app file...")
    app_file: Path = Path("build") / "app.py"
    app_file.write_text(
        VERSION_PATTERN.sub(project_version, app_file.read_text(encoding="utf8"))
    )


def generate_nuitka_cmd() -> list[str]:
    return [
        ".venv\\scripts\\nuitka",
        "--msvc=latest",
        "--standalone",
        "--remove-output",
        "--windows-console-mode=attach",
        f"--company-name={project_author}",
        f"--copyright={project_author}",
        f"--product-name={project_name}",
        f"--file-description={project_name}",
        f"--file-version={project_version.split('-')[0]}",
        f"--product-version={project_version.split('-')[0]}",
        "--nofollow-import-to=tkinter",
        "--output-filename=iris.exe",
        "build/main.py",
    ]


def build() -> None:
    logging.info("Building application with nuitka...")

    prepare_src()
    cmd: list[str] = generate_nuitka_cmd()

    logging.info(f"Running command: {' '.join(cmd)!r}")
    retcode: int = subprocess.run(cmd, shell=True).returncode
    if retcode != 0:
        raise Exception("Failed to build application with nuitka")


try:
    build()
except Exception as ex:
    logging.error(f"Failed to build application with nuitka: {str(ex)}", exc_info=ex)

    shutil.rmtree("dist", ignore_errors=True)

else:
    shutil.rmtree("build", ignore_errors=True)
    logging.debug("Deleted build directory.")
