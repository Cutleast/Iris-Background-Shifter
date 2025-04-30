"""
Copyright (c) Cutleast

Enum for process changes
"""

from enum import Enum, auto


class ProcessState(Enum):
    """Enum for process changes"""

    Started = auto()
    """Indicates that a process has started"""

    Stopped = auto()
    """Indicates that a process has stopped"""
