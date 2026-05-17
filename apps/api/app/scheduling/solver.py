from dataclasses import dataclass
from datetime import datetime

from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.domain.tasks import FlexibleTask
from app.scheduling.domain.time import require_aware


class SolverInputError(ValueError):
    pass


@dataclass(frozen=True)
class TimeWindow:
    start: datetime
    end: datetime

    @property
    def minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


@dataclass(frozen=True)
class PlanningInput:
    horizon_start: datetime
    horizon_end: datetime
    tasks: tuple[FlexibleTask, ...]
    fixed_events: tuple[FixedEventWindow, ...]
    availability: tuple[TimeWindow, ...]


def validate_window(window: TimeWindow) -> TimeWindow:
    require_aware(window.start)
    require_aware(window.end)
    if window.start >= window.end:
        raise SolverInputError("time window is reversed")
    return window


def merge_windows(windows: list[TimeWindow]) -> list[TimeWindow]:
    if not windows:
        return []

    ordered = sorted(
        (validate_window(window) for window in windows), key=lambda x: x.start
    )
    merged = [ordered[0]]

    for window in ordered[1:]:
        previous = merged[-1]
        if window.start <= previous.end:
            merged[-1] = TimeWindow(previous.start, max(previous.end, window.end))
        else:
            merged.append(window)

    return merged


def subtract_window(
    windows: list[TimeWindow],
    blocked: TimeWindow,
) -> list[TimeWindow]:
    validate_window(blocked)
    remaining: list[TimeWindow] = []

    for window in windows:
        if blocked.end <= window.start or blocked.start >= window.end:
            remaining.append(window)
            continue
        if blocked.start > window.start:
            remaining.append(TimeWindow(window.start, blocked.start))
        if blocked.end < window.end:
            remaining.append(TimeWindow(blocked.end, window.end))

    return remaining


def build_free_windows(planning: PlanningInput) -> list[TimeWindow]:
    require_aware(planning.horizon_start)
    require_aware(planning.horizon_end)
    if planning.horizon_start >= planning.horizon_end:
        raise SolverInputError("planning horizon is reversed")

    free = merge_windows(
        [
            TimeWindow(
                max(window.start, planning.horizon_start),
                min(window.end, planning.horizon_end),
            )
            for window in planning.availability
            if window.end > planning.horizon_start
            and window.start < planning.horizon_end
        ]
    )

    for event in planning.fixed_events:
        blocked = TimeWindow(event.blocked_start, event.blocked_end)
        free = subtract_window(free, blocked)

    return free
