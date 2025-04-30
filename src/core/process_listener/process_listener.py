"""
Copyright (c) Cutleast

Class for listening to process changes (start, stop).
"""

import logging
import time
from collections.abc import Callable

import psutil

from .process_state import ProcessState

ProcessCallback = Callable[[str, ProcessState], None]
"""A function or method accepting a string and a ProcessState as arguments."""


class ProcessListener:
    """
    Class for listening to process changes (start, stop).
    """

    __process_names_to_watch: set[str]
    __process_states: dict[str, ProcessState] = {}
    __callbacks: set[ProcessCallback]
    __running: bool = True

    log: logging.Logger = logging.getLogger("ProcessListener")

    def __init__(
        self,
        process_names_to_watch: list[str],
        initial_callbacks: list[ProcessCallback] = [],
    ) -> None:
        self.__process_names_to_watch = set(process_names_to_watch)
        self.__callbacks = set(initial_callbacks)

    def run(self, interval: float = 10.0) -> None:
        """
        Runs a check for process changes in the specified interval (seconds).

        Args:
            interval (float, optional): Check interval in seconds. Defaults to 10.0.
        """

        self.log.info("Process listener started.")

        while self.__running:
            self.__check()
            time.sleep(interval)

        self.log.info("Process listener stopped.")

    def stop(self) -> None:
        """
        Stops the process listener.
        """

        self.__running = False

    def __check(self) -> None:
        # self.log.info("Checking for process changes...")
        running_processes: list[str] = ProcessListener.get_running_processes()
        # self.log.debug(f"Running processes: {len(running_processes)}")

        for process_name in self.__process_names_to_watch:
            if process_name in running_processes:
                if self.__process_states.get(process_name) != ProcessState.Started:
                    self.__process_states[process_name] = ProcessState.Started
                    self.log.debug(f"Process started: {process_name}")
                    for callback in self.__callbacks:
                        callback(process_name, ProcessState.Started)
            else:
                if (
                    process_name in self.__process_states
                    and self.__process_states.get(process_name) != ProcessState.Stopped
                ):
                    self.__process_states[process_name] = ProcessState.Stopped
                    self.log.debug(f"Process stopped: {process_name}")
                    for callback in self.__callbacks:
                        callback(process_name, ProcessState.Stopped)

        # self.log.debug("Check complete.")

    def add_process_name(self, process_name: str) -> None:
        """
        Adds a process name to the list of processes to watch.

        Args:
            process_name (str): The process name
        """

        self.__process_names_to_watch.add(process_name)

    def rem_process_name(self, process_name: str) -> None:
        """
        Removes a process name from the list of processes to watch.

        Raises:
            KeyError: If the process name is not found

        Args:
            process_name (str): The process name
        """

        self.__process_names_to_watch.remove(process_name)

    def add_callback(self, callback: ProcessCallback) -> None:
        """
        Adds a callback to the list of callbacks.

        Args:
            callback (ProcessCallback): The callback
        """

        self.__callbacks.add(callback)

    def rem_callback(self, callback: ProcessCallback) -> None:
        """
        Removes a callback from the list of callbacks.

        Raises:
            KeyError: If the callback is not found

        Args:
            callback (ProcessCallback): The callback
        """

        self.__callbacks.remove(callback)

    @staticmethod
    def get_running_processes() -> list[str]:
        """
        Returns a list of currently running processes.

        Returns:
            list[str]: List of running processes
        """

        return [process.name() for process in psutil.process_iter()]
