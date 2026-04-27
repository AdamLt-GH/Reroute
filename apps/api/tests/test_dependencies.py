from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from app.scheduling.domain.dependencies import (
    Dependency,
    DependencyCycleError,
    DependencyError,
    build_dependency_graph,
    order_dependency_graph,
    validate_acyclic,
    validate_task_dependencies,
)
from app.scheduling.domain.tasks import FlexibleTask


def test_dependency_graph_keeps_each_task() -> None:
    research = uuid4()
    report = uuid4()

    graph = build_dependency_graph(
        [research, report],
        [Dependency(research, report)],
    )

    assert graph[research] == {report}
    assert graph[report] == set()


def test_dependency_graph_rejects_self_dependencies() -> None:
    task_id = uuid4()

    with pytest.raises(DependencyError, match="cannot depend on itself"):
        build_dependency_graph(
            [task_id],
            [Dependency(task_id, task_id)],
        )


def test_dependency_order_places_prerequisites_first() -> None:
    research = uuid4()
    analysis = uuid4()
    report = uuid4()
    graph = build_dependency_graph(
        [research, analysis, report],
        [
            Dependency(research, analysis),
            Dependency(analysis, report),
        ],
    )

    result = order_dependency_graph(graph)

    assert result.ordered == (research, analysis, report)
    assert result.blocked == ()


def test_dependency_cycles_are_rejected_with_the_blocked_tasks() -> None:
    first = uuid4()
    second = uuid4()
    graph = build_dependency_graph(
        [first, second],
        [
            Dependency(first, second),
            Dependency(second, first),
        ],
    )

    with pytest.raises(DependencyCycleError) as error:
        validate_acyclic(graph)

    assert set(error.value.task_ids) == {first, second}


def task(task_id: UUID) -> FlexibleTask:
    start = datetime(2026, 4, 27, 18, 0, tzinfo=UTC)
    return FlexibleTask(
        id=task_id,
        title="Task",
        estimated_minutes=60,
        remaining_minutes=60,
        earliest_start=start,
        deadline=start + timedelta(days=2),
        minimum_session_minutes=30,
        maximum_session_minutes=60,
        preferred_session_minutes=60,
        splittable=False,
    )


def test_task_dependency_validation_returns_tasks_in_working_order() -> None:
    first = uuid4()
    second = uuid4()
    tasks = {first: task(first), second: task(second)}

    ordered = validate_task_dependencies(
        tasks,
        [Dependency(first, second)],
    )

    assert [item.id for item in ordered] == [first, second]
