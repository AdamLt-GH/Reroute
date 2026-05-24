from dataclasses import dataclass
from datetime import date, datetime, timedelta
from uuid import UUID

from app.scheduling.domain.dependencies import (
    Dependency,
    validate_task_dependencies,
)
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
    dependencies: tuple[Dependency, ...] = ()
    maximum_daily_minutes: int = 480


@dataclass(frozen=True)
class ScheduledBlock:
    task_id: UUID
    title: str
    start: datetime
    end: datetime

    @property
    def minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


@dataclass(frozen=True)
class ScheduleResult:
    blocks: tuple[ScheduledBlock, ...]
    unscheduled_task_ids: tuple[UUID, ...]


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


def choose_session_minutes(
    task: FlexibleTask,
    remaining_minutes: int,
    available_minutes: int,
) -> int:
    if not task.splittable:
        return remaining_minutes if remaining_minutes <= available_minutes else 0

    session = min(
        remaining_minutes,
        available_minutes,
        task.maximum_session_minutes,
        task.preferred_session_minutes,
    )
    leftover = remaining_minutes - session
    if 0 < leftover < task.minimum_session_minutes:
        session -= task.minimum_session_minutes - leftover

    return session if session >= task.minimum_session_minutes else 0


def schedule_tasks(planning: PlanningInput) -> ScheduleResult:
    if planning.maximum_daily_minutes <= 0:
        raise SolverInputError("daily work limit must be positive")

    free = build_free_windows(planning)
    blocks: list[ScheduledBlock] = []
    unscheduled: list[UUID] = []
    daily_minutes: dict[date, int] = {}
    if planning.dependencies:
        task_map = {task.id: task for task in planning.tasks}
        ordered_tasks = validate_task_dependencies(
            task_map,
            planning.dependencies,
        )
    else:
        ordered_tasks = tuple(sorted(planning.tasks, key=lambda item: item.deadline))

    for task in ordered_tasks:
        remaining = task.remaining_minutes

        while remaining > 0:
            placed = False
            for window in free:
                start = max(window.start, task.earliest_start)
                end_limit = min(window.end, task.deadline)
                available = int((end_limit - start).total_seconds() // 60)
                used_today = daily_minutes.get(start.date(), 0)
                available = min(
                    available,
                    planning.maximum_daily_minutes - used_today,
                )
                session = choose_session_minutes(task, remaining, available)
                if session == 0:
                    continue

                end = start + timedelta(minutes=session)
                blocks.append(ScheduledBlock(task.id, task.title, start, end))
                free = subtract_window(free, TimeWindow(start, end))
                remaining -= session
                daily_minutes[start.date()] = used_today + session
                placed = True
                break

            if not placed:
                unscheduled.append(task.id)
                break

    return ScheduleResult(
        blocks=tuple(sorted(blocks, key=lambda block: block.start)),
        unscheduled_task_ids=tuple(unscheduled),
    )
