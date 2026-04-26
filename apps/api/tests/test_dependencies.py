from uuid import uuid4

import pytest

from app.scheduling.domain.dependencies import (
    Dependency,
    DependencyError,
    build_dependency_graph,
    order_dependency_graph,
)


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
