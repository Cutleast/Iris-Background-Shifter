"""
Copyright (c) Cutleast
"""

import sys
from argparse import ArgumentParser, Namespace

from app import App


def __init_argparser() -> ArgumentParser:
    """
    Initializes commandline argument parser.
    """

    parser = ArgumentParser(
        prog=sys.executable, description=f"{App.NAME} v{App.VERSION} (c) {App.AUTHOR}"
    )

    parser.add_argument(
        "-p",
        "--index-path",
        nargs="?",
        default="",
        help="Overrides the path to the index file.",
    )

    parser.add_argument(
        "-i",
        "--interval",
        nargs="?",
        default="",
        help="Overrides the interval in seconds to check for process changes. Defaults to 1.0.",
    )

    return parser


if __name__ == "__main__":
    parser: ArgumentParser = __init_argparser()
    arg_namespace: Namespace = parser.parse_args()

    App(arg_namespace).exec(float(arg_namespace.interval or 1))
