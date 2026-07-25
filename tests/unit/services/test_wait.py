import bootstrap

import pytest

from gameboy_automation.services.wait import (
    WaitTimeoutError,
    wait_until,
)


def test_wait_until_returns_immediately() -> None:
    result = wait_until(
        lambda: "success",
    )

    assert result == "success"


def test_wait_until_retries_until_success() -> None:
    attempts = 0

    def condition() -> str | None:
        nonlocal attempts

        attempts += 1

        if attempts < 3:
            return None

        return "done"

    result = wait_until(
        condition,
        poll_interval_seconds=0.0,
    )

    assert result == "done"
    assert attempts == 3


def test_wait_until_times_out() -> None:
    with pytest.raises(WaitTimeoutError):
        wait_until(
            lambda: None,
            timeout_seconds=0.01,
            poll_interval_seconds=0.0,
        )


def test_wait_until_rejects_invalid_timeout() -> None:
    with pytest.raises(ValueError):
        wait_until(
            lambda: "done",
            timeout_seconds=0.0,
        )


def test_wait_until_rejects_negative_poll_interval() -> None:
    with pytest.raises(ValueError):
        wait_until(
            lambda: "done",
            poll_interval_seconds=-1.0,
        )