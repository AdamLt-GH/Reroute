from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID


class DependencyError(ValueError):
    pass


@dataclass(frozen=True)
class Dependency:
    prerequisite_id: UUID
    dependent_id: UUID


def build_dependency_graph(
    task_ids: Iterable[UUID],
    dependencies: Iterable[Dependency],
) -> dict[UUID, set[UUID]]:
    graph: dict[UUID, set[UUID]] = {task_id: set() for task_id in task_ids}

    for dependency in dependencies:
        if dependency.prerequisite_id == dependency.dependent_id:
            raise DependencyError("a task cannot depend on itself")
        if dependency.prerequisite_id not in graph:
            raise DependencyError("prerequisite task is missing")
        if dependency.dependent_id not in graph:
            raise DependencyError("dependent task is missing")

        graph[dependency.prerequisite_id].add(dependency.dependent_id)

    return graph
