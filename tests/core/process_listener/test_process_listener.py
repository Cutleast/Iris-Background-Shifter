"""
Copyright (c) Cutleast

Tests for the ProcessListener class
"""

from collections.abc import Callable

import pytest
from base_test import BaseTest
from utils import Utils

from core.process_listener.process_listener import ProcessListener
from core.process_listener.process_state import ProcessState


class TestProcessListener(BaseTest):
    """
    Tests for the `core.process_listener.process_listener.ProcessListener` class.
    """

    PROCESS_STATES: tuple[str, type[dict[str, ProcessState]]] = ("process_states", dict)
    """Identifier for accessing the private process_states field."""

    def test_check(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
        Tests the private `ProcessListener.check` method.
        """

        # given
        process_listener = ProcessListener(["test.executable", "test3.executable"])
        check_method: Callable[[], None] = Utils.get_private_method(
            process_listener, TestProcessListener.CHECK, lambda: None
        )
        process_states: dict[str, ProcessState] = Utils.get_private_field(
            process_listener, *TestProcessListener.PROCESS_STATES
        )
        running_processes: list[str] = [
            "test.executable",
            "test.executable",
            "test4.executable",
        ]

        # Patch ProcessListener.get_running_processes() to return a custom list
        monkeypatch.setattr(
            ProcessListener, "get_running_processes", lambda: running_processes
        )

        # then
        assert process_states == {}

        # when
        check_method()

        # then
        assert process_states == {"test.executable": ProcessState.Started}

        # when
        running_processes.remove("test.executable")
        running_processes.append("test2.executable")
        check_method()

        # then
        assert process_states == {"test.executable": ProcessState.Started}

        # when
        running_processes.remove("test.executable")
        check_method()

        # then
        assert process_states == {"test.executable": ProcessState.Stopped}

        monkeypatch.undo()

    def test_check_callback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
        Tests the correct handling of the callbacks passed to the constructor when running the check.
        """

        # given
        calls: list[tuple[str, ProcessState]] = []

        def callback(name: str, state: ProcessState) -> None:
            return calls.append((name, state))

        process_listener = ProcessListener(
            ["test.executable", "test3.executable"], [callback]
        )
        running_processes: list[str] = []
        check_method: Callable[[], None] = Utils.get_private_method(
            process_listener, TestProcessListener.CHECK, lambda: None
        )

        # Patch ProcessListener.get_running_processes() to return a custom list
        monkeypatch.setattr(
            ProcessListener, "get_running_processes", lambda: running_processes
        )

        # when
        check_method()

        # then
        assert calls == []

        # when
        running_processes.append("test.executable")
        check_method()

        # then
        assert calls == [("test.executable", ProcessState.Started)]

        # when
        running_processes.remove("test.executable")
        check_method()

        # then
        assert calls[-1] == ("test.executable", ProcessState.Stopped)

        # when
        running_processes.append("test.executable")
        process_listener.rem_callback(callback)
        check_method()

        # then
        assert calls == [
            ("test.executable", ProcessState.Started),
            ("test.executable", ProcessState.Stopped),
        ]

        # when
        running_processes.remove("test.executable")
        process_listener.add_callback(callback)
        # Test that the callback is not called multiple times when there is no change
        for _ in range(5):
            check_method()

        # then
        assert calls == [
            ("test.executable", ProcessState.Started),
            ("test.executable", ProcessState.Stopped),
            ("test.executable", ProcessState.Stopped),
        ]

        monkeypatch.undo()
