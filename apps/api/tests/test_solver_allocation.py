from datetime import UTC, datetime
from uuid import uuid4

from app.scheduling.domain.tasks import FlexibleTask
from app.scheduling.solver import (
    PlanningInput,
    TimeWindow,
    schedule_tasks,
)


def test_splittable_tasks_are_placed_in_multiple_sessions() -> None:
    start = datetime(2026, 5, 23, 9, tzinfo=UTC)
    task = FlexibleTask(
        id=uuid4(),
        title="Write report",
        estimated_minutes=150,
        remaining_minutes=150,
        earliest_start=start,
        deadline=datetime(2026, 5, 23, 17, tzinfo=UTC),
        minimum_session_minutes=30,
        preferred_session_minutes=60,
        maximum_session_minutes=90,
        splittable=True,
    )
    planning = PlanningInput(
        horizon_start=start,
        horizon_end=datetime(2026, 5, 23, 18, tzinfo=UTC),
        tasks=(task,),
        fixed_events=(),
        availability=(TimeWindow(start, datetime(2026, 5, 23, 13, tzinfo=UTC)),),
    )

    result = schedule_tasks(planning)

    assert [block.minutes for block in result.blocks] == [60, 60, 30]
    assert result.unscheduled_task_ids == ()


def test_tasks_that_do_not_fit_are_reported() -> None:
    start = datetime(2026, 5, 23, 9, tzinfo=UTC)
    task = FlexibleTask(
        id=uuid4(),
        title="Large assignment",
        estimated_minutes=180,
        remaining_minutes=180,
        earliest_start=start,
        deadline=datetime(2026, 5, 23, 12, tzinfo=UTC),
        minimum_session_minutes=30,
        preferred_session_minutes=60,
        maximum_session_minutes=180,
        splittable=False,
    )
    planning = PlanningInput(
        horizon_start=start,
        horizon_end=datetime(2026, 5, 23, 12, tzinfo=UTC),
        tasks=(task,),
        fixed_events=(),
        availability=(TimeWindow(start, datetime(2026, 5, 23, 11, tzinfo=UTC)),),
    )

    result = schedule_tasks(planning)

    assert result.blocks == ()
    assert result.unscheduled_task_ids == (task.id,)


def test_blocks_stay_between_the_earliest_start_and_deadline() -> None:
    available_start = datetime(2026, 5, 23, 8, tzinfo=UTC)
    task = FlexibleTask(
        id=uuid4(),
        title="Prepare slides",
        estimated_minutes=60,
        remaining_minutes=60,
        earliest_start=datetime(2026, 5, 23, 10, tzinfo=UTC),
        deadline=datetime(2026, 5, 23, 12, tzinfo=UTC),
        minimum_session_minutes=30,
        preferred_session_minutes=60,
        maximum_session_minutes=60,
        splittable=True,
    )
    planning = PlanningInput(
        horizon_start=available_start,
        horizon_end=datetime(2026, 5, 23, 18, tzinfo=UTC),
        tasks=(task,),
        fixed_events=(),
        availability=(
            TimeWindow(
                available_start,
                datetime(2026, 5, 23, 18, tzinfo=UTC),
            ),
        ),
    )

    result = schedule_tasks(planning)

    assert result.blocks[0].start == task.earliest_start
    assert result.blocks[0].end <= task.deadline
