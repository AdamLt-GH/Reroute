from datetime import datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.availability import AvailabilityWindow
from app.models.event import FixedEvent
from app.models.preference import SchedulingConstraint
from app.models.schedule import Schedule, ScheduleBlock
from app.models.task import Task, TaskDependency
from app.models.user import User
from app.scheduling.domain.dependencies import Dependency
from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.domain.tasks import (
    FlexibleTask,
    TaskDifficulty,
    TaskPriority,
    TaskStatus,
)
from app.scheduling.solver import PlanningInput, TimeWindow, schedule_tasks
from app.schemas.schedules import (
    ScheduleGenerateRequest,
    ScheduleRecalculateRequest,
)


class ScheduleNotFoundError(ValueError):
    pass


def expand_availability(
    records: list[AvailabilityWindow],
    start: datetime,
    end: datetime,
    timezone_name: str,
) -> tuple[TimeWindow, ...]:
    timezone = ZoneInfo(timezone_name)
    current = start.astimezone(timezone).date()
    last = end.astimezone(timezone).date()
    windows: list[TimeWindow] = []

    while current <= last:
        for record in records:
            if record.day_of_week != current.weekday():
                continue
            if record.effective_from and current < record.effective_from:
                continue
            if record.effective_until and current > record.effective_until:
                continue
            windows.append(
                TimeWindow(
                    datetime.combine(current, record.start_time, timezone),
                    datetime.combine(current, record.end_time, timezone),
                )
            )
        current += timedelta(days=1)

    return tuple(windows)


class ScheduleService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self, user_id: UUID) -> list[Schedule]:
        result = await self._session.scalars(
            select(Schedule)
            .where(Schedule.user_id == user_id)
            .options(selectinload(Schedule.blocks))
            .order_by(Schedule.created_at.desc())
        )
        return list(result)

    async def generate(
        self,
        user: User,
        request: ScheduleGenerateRequest,
        *,
        source: str = "initial",
        parent_schedule_id: UUID | None = None,
    ) -> Schedule:
        tasks = list(
            await self._session.scalars(select(Task).where(Task.user_id == user.id))
        )
        active_tasks = [task for task in tasks if task.remaining_minutes > 0]
        task_ids = {task.id for task in active_tasks}
        events = list(
            await self._session.scalars(
                select(FixedEvent).where(FixedEvent.user_id == user.id)
            )
        )
        availability = list(
            await self._session.scalars(
                select(AvailabilityWindow).where(AvailabilityWindow.user_id == user.id)
            )
        )
        dependencies = list(
            await self._session.scalars(
                select(TaskDependency).where(
                    TaskDependency.prerequisite_id.in_(task_ids),
                    TaskDependency.dependent_id.in_(task_ids),
                )
            )
        )
        constraints = list(
            await self._session.scalars(
                select(SchedulingConstraint).where(
                    SchedulingConstraint.user_id == user.id,
                    SchedulingConstraint.enabled.is_(True),
                )
            )
        )
        maximum_daily = 480
        for constraint in constraints:
            if constraint.kind == "maximum_daily_work":
                value = constraint.settings.get("minutes")
                if isinstance(value, int):
                    maximum_daily = value

        planning = PlanningInput(
            horizon_start=request.horizon_start,
            horizon_end=request.horizon_end,
            tasks=tuple(
                FlexibleTask(
                    id=task.id,
                    title=task.title,
                    estimated_minutes=task.estimated_minutes,
                    remaining_minutes=task.remaining_minutes,
                    earliest_start=task.earliest_start,
                    deadline=task.deadline,
                    minimum_session_minutes=task.minimum_session_minutes,
                    preferred_session_minutes=task.preferred_session_minutes,
                    maximum_session_minutes=task.maximum_session_minutes,
                    splittable=task.splittable,
                    priority=TaskPriority(task.priority),
                    difficulty=TaskDifficulty(task.difficulty),
                    status=TaskStatus(task.status),
                    actual_minutes=task.actual_minutes,
                )
                for task in active_tasks
            ),
            fixed_events=tuple(
                FixedEventWindow(
                    id=event.id,
                    title=event.title,
                    start=event.start_at,
                    end=event.end_at,
                    travel_before_minutes=event.travel_before_minutes,
                    travel_after_minutes=event.travel_after_minutes,
                )
                for event in events
            ),
            availability=expand_availability(
                availability,
                request.horizon_start,
                request.horizon_end,
                user.timezone,
            ),
            dependencies=tuple(
                Dependency(item.prerequisite_id, item.dependent_id)
                for item in dependencies
            ),
            maximum_daily_minutes=maximum_daily,
        )
        result = schedule_tasks(planning)
        schedule = Schedule(
            user_id=user.id,
            horizon_start=request.horizon_start,
            horizon_end=request.horizon_end,
            status="proposed",
            source=source,
            parent_schedule_id=parent_schedule_id,
            unscheduled_task_ids=[
                str(task_id) for task_id in result.unscheduled_task_ids
            ],
            blocks=[
                ScheduleBlock(
                    task_id=block.task_id,
                    title=block.title,
                    start_at=block.start,
                    end_at=block.end,
                )
                for block in result.blocks
            ],
        )
        self._session.add(schedule)
        await self._session.flush()
        return schedule

    async def accept(self, user_id: UUID, schedule_id: UUID) -> Schedule:
        schedule = await self._session.scalar(
            select(Schedule)
            .where(Schedule.id == schedule_id, Schedule.user_id == user_id)
            .options(selectinload(Schedule.blocks))
        )
        if schedule is None:
            raise ScheduleNotFoundError

        await self._session.execute(
            update(Schedule)
            .where(Schedule.user_id == user_id, Schedule.status == "accepted")
            .values(status="archived")
        )
        schedule.status = "accepted"
        task_ids = [block.task_id for block in schedule.blocks if block.task_id]
        if task_ids:
            await self._session.execute(
                update(Task).where(Task.id.in_(task_ids)).values(status="scheduled")
            )
        await self._session.flush()
        return schedule

    async def recalculate(
        self,
        user: User,
        schedule_id: UUID,
        request: ScheduleRecalculateRequest,
    ) -> Schedule:
        original = await self._session.scalar(
            select(Schedule).where(
                Schedule.id == schedule_id,
                Schedule.user_id == user.id,
            )
        )
        if original is None:
            raise ScheduleNotFoundError

        self._session.add(
            FixedEvent(
                user_id=user.id,
                title=request.title,
                start_at=request.start_at,
                end_at=request.end_at,
                source="disruption",
                locked=True,
                travel_before_minutes=0,
                travel_after_minutes=0,
            )
        )
        original.status = "replaced"
        await self._session.flush()
        return await self.generate(
            user,
            ScheduleGenerateRequest(
                horizon_start=original.horizon_start,
                horizon_end=original.horizon_end,
            ),
            source="recalculation",
            parent_schedule_id=original.id,
        )
