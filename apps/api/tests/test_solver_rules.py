from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.scheduling.domain.dependencies import Dependency
from app.scheduling.domain.tasks import FlexibleTask
from app.scheduling.solver import PlanningInput, TimeWindow, schedule_tasks


def make_task(
    task_id: UUID,
    title: str,
    deadline_hour: int,
) -> FlexibleTask:
    start = datetime(2026, 5, 24, 9, tzinfo=UTC)
    return FlexibleTask(
        id=task_id,
        title=title,
        estimated_minutes=60,
        remaining_minutes=60,
        earliest_start=start,
        deadline=datetime(2026, 5, 24, deadline_hour, tzinfo=UTC),
        minimum_session_minutes=30,
        preferred_session_minutes=60,
        maximum_session_minutes=60,
        splittable=True,
    )


def test_prerequisites_are_scheduled_before_dependent_tasks() -> None:
    first_id = uuid4()
    second_id = uuid4()
    first = make_task(first_id, "Research", 17)
    second = make_task(second_id, "Write report", 12)
    planning = PlanningInput(
        horizon_start=datetime(2026, 5, 24, 9, tzinfo=UTC),
        horizon_end=datetime(2026, 5, 24, 18, tzinfo=UTC),
        tasks=(first, second),
        fixed_events=(),
        availability=(
            TimeWindow(
                datetime(2026, 5, 24, 9, tzinfo=UTC),
                datetime(2026, 5, 24, 18, tzinfo=UTC),
            ),
        ),
        dependencies=(Dependency(first_id, second_id),),
    )

    result = schedule_tasks(planning)

    assert [block.title for block in result.blocks] == [
        "Research",
        "Write report",
    ]


def test_daily_work_limit_leaves_extra_work_unscheduled() -> None:
    first = make_task(uuid4(), "Research", 17)
    second = make_task(uuid4(), "Write report", 17)
    planning = PlanningInput(
        horizon_start=datetime(2026, 5, 24, 9, tzinfo=UTC),
        horizon_end=datetime(2026, 5, 24, 18, tzinfo=UTC),
        tasks=(first, second),
        fixed_events=(),
        availability=(
            TimeWindow(
                datetime(2026, 5, 24, 9, tzinfo=UTC),
                datetime(2026, 5, 24, 18, tzinfo=UTC),
            ),
        ),
        maximum_daily_minutes=60,
    )

    result = schedule_tasks(planning)

    assert len(result.blocks) == 1
    assert len(result.unscheduled_task_ids) == 1
