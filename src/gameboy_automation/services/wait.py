from __future__ import annotations

from collections.abc import Callable
from time import monotonic, sleep
from typing import TypeVar


Result = TypeVar("Result")


class WaitTimeoutError(TimeoutError):
    """Raised when a condition does not succeed before its timeout."""


def wait_until(
    condition: Callable[[], Result | None],
    *,
    timeout_seconds: float = 10.0,
    poll_interval_seconds: float = 0.1,
    description: str = "condition",
) -> Result:
    """
    Repeatedly evaluate a condition until it returns a non-None result.

    Args:
        condition:
            Function called repeatedly. Return None while waiting and return
            a value when the condition succeeds.
        timeout_seconds:
            Maximum amount of time to wait.
        poll_interval_seconds:
            Delay between condition checks.
        description:
            Human-readable condition name used in timeout errors.

    Returns:
        The first non-None value returned by the condition.

    Raises:
        ValueError:
            If timeout_seconds or poll_interval_seconds is invalid.
        WaitTimeoutError:
            If the condition does not succeed before the timeout.
    """
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero.")

    if poll_interval_seconds < 0:
        raise ValueError(
            "poll_interval_seconds cannot be negative."
        )

    deadline = monotonic() + timeout_seconds

    while True:
        result = condition()

        if result is not None:
            return result

        if monotonic() >= deadline:
            raise WaitTimeoutError(
                f"Timed out after {timeout_seconds:.2f} seconds "
                f"while waiting for {description}."
            )

        sleep(poll_interval_seconds)