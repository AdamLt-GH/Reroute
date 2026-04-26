from uuid import uuid4

import pytest

from app.scheduling.domain.dependencies import (
    Dependency,
    DependencyError,
    build_dependency_graph,
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
