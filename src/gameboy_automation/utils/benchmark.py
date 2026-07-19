from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import List, Optional, Tuple


_SECONDS_PER_MINUTE = 60
_SECONDS_PER_HOUR = 60 * _SECONDS_PER_MINUTE
_SECONDS_PER_DAY = 24 * _SECONDS_PER_HOUR
_SECONDS_PER_WEEK = 7 * _SECONDS_PER_DAY


def _plural(n: int, singular: str, plural: Optional[str] = None) -> str:
    if n == 1:
        return singular
    return plural if plural is not None else f"{singular}s"


def _split_seconds(total_seconds: float) -> Tuple[int, int, int, int, int, int]:
    """
    Convert a float duration (seconds) into:
    (weeks, days, hours, minutes, seconds, microseconds)
    """
    if total_seconds < 0:
        total_seconds = 0.0

    whole = int(total_seconds)
    microseconds = int(round((total_seconds - whole) * 1_000_000))

    # Normalize microseconds overflow due to rounding
    if microseconds >= 1_000_000:
        whole += 1
        microseconds -= 1_000_000

    weeks, rem = divmod(whole, _SECONDS_PER_WEEK)
    days, rem = divmod(rem, _SECONDS_PER_DAY)
    hours, rem = divmod(rem, _SECONDS_PER_HOUR)
    minutes, seconds = divmod(rem, _SECONDS_PER_MINUTE)

    return weeks, days, hours, minutes, seconds, microseconds


def humanize_duration(
    total_seconds: float,
    *,
    include_microseconds: bool = True,
    compact: bool = False,
) -> str:
    """
    Format seconds into a human-readable string.

    Examples:
      - "2 Minutes 3 Seconds 1200 Microseconds"
      - "1 Hour 0 Minutes 5 Seconds" (microseconds omitted)
      - compact=True => "1h 2m 3s"
    """
    w, d, h, m, s, us = _split_seconds(total_seconds)

    if compact:
        parts: List[str] = []
        if w: parts.append(f"{w}w")
        if d: parts.append(f"{d}d")
        if h: parts.append(f"{h}h")
        if m: parts.append(f"{m}m")
        if s or not parts: parts.append(f"{s}s")
        if include_microseconds and us: parts.append(f"{us}us")
        return " ".join(parts)

    parts = []
    if w: parts.append(f"{w} {_plural(w, 'Week')}")
    if d: parts.append(f"{d} {_plural(d, 'Day')}")
    if h: parts.append(f"{h} {_plural(h, 'Hour')}")
    if m: parts.append(f"{m} {_plural(m, 'Minute')}")
    if s or not parts: parts.append(f"{s} {_plural(s, 'Second')}")
    if include_microseconds:
        parts.append(f"{us} {_plural(us, 'Microsecond')}")

    return " ".join(parts)


@dataclass
class Benchmark:
    """
    A small benchmarking utility.

    Primary API:
      - start()/reset()
      - lap(label)
      - stop()
      - elapsed_seconds (property)
      - human_readable(...)

    Supports:
      - context manager: with Benchmark("load") as b: ...
    """
    name: str = "benchmark"
    autostart: bool = True

    _start: Optional[float] = field(default=None, init=False, repr=False)
    _end: Optional[float] = field(default=None, init=False, repr=False)
    _laps: List[Tuple[str, float]] = field(default_factory=list, init=False, repr=False)
    counter_reset: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.autostart:
            self.start()

    def __enter__(self) -> "Benchmark":
        if self._start is None:
            self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    @property
    def running(self) -> bool:
        return self._start is not None and self._end is None

    def start(self) -> "Benchmark":
        self._start = perf_counter()
        self._end = None
        self._laps.clear()
        return self

    def reset(self) -> "Benchmark":
        self.counter_reset += 1
        return self.start()

    def stop(self) -> float:
        """
        Stops the timer and returns elapsed seconds.
        Calling stop() multiple times is safe (idempotent).
        """
        if self._start is None:
            # Treat "never started" as 0 seconds
            self._start = perf_counter()
            self._end = self._start
            return 0.0

        if self._end is None:
            self._end = perf_counter()
        return self.elapsed_seconds

    # Backwards-friendly alias (your old class had both stop() and end()).
    def end(self) -> float:
        return self.stop()

    @property
    def elapsed_seconds(self) -> float:
        if self._start is None:
            return 0.0
        end = self._end if self._end is not None else perf_counter()
        return max(0.0, end - self._start)

    def lap(self, label: str) -> float:
        """
        Records a split time since start. Returns the split elapsed seconds.
        """
        split = self.elapsed_seconds
        self._laps.append((label, split))
        return split

    @property
    def laps(self) -> Tuple[Tuple[str, float], ...]:
        return tuple(self._laps)

    def human_readable(
        self,
        *,
        include_microseconds: bool = True,
        compact: bool = False,
    ) -> str:
        return humanize_duration(
            self.elapsed_seconds,
            include_microseconds=include_microseconds,
            compact=compact,
        )

    def __str__(self) -> str:
        return f"{self.name}: {self.human_readable(include_microseconds=True)}"

    # Compatibility helpers for code that used your old method names.
    def human_readable_string(self) -> str:
        return self.human_readable(include_microseconds=True, compact=False)

    def human_readable_string_without_microseconds(self) -> str:
        return self.human_readable(include_microseconds=False, compact=False)

    def get_runtime_seconds(self) -> int:
        """
        Old code returned integer seconds (truncating).
        """
        return int(self.elapsed_seconds)

    def seconds_to_human_readable(self, seconds: int, return_type: str = "string"):
        """
        A cleaned-up version of your old helper.
        """
        if not isinstance(seconds, int):
            if return_type == "string":
                return "Please call 'seconds_to_human_readable' with an integer"
            return 0

        if return_type == "string":
            return humanize_duration(float(seconds), include_microseconds=False, compact=False).strip()
        return seconds
