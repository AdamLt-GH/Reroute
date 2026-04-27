from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from uuid import UUID

from app.scheduling.domain.tasks import FlexibleTask


class DependencyError(ValueError):
    pass


class DependencyCycleError(DependencyError):
    def __init__(self, task_ids: tuple[UUID, ...]) -> None:
        super().__init__("task dependencies contain a cycle")
        self.task_ids = task_ids


@dataclass(frozen=True)
class Dependency:
    prerequisite_id: UUID
    dependent_id: UUID


@dataclass(frozen=True)
class DependencyOrder:
    ordered: tuple[UUID, ...]
    blocked: tuple[UUID, ...]


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


def order_dependency_graph(
    graph: dict[UUID, set[UUID]],
) -> DependencyOrder:
    incoming = {task_id: 0 for task_id in graph}

    for dependents in graph.values():
        for dependent_id in dependents:
            incoming[dependent_id] += 1

    ready = sorted(
        (task_id for task_id, count in incoming.items() if count == 0),
        key=str,
    )
    ordered: list[UUID] = []

    while ready:
        task_id = ready.pop(0)
        ordered.append(task_id)

        for dependent_id in sorted(graph[task_id], key=str):
            incoming[dependent_id] -= 1
            if incoming[dependent_id] == 0:
                ready.append(dependent_id)
                ready.sort(key=str)

    blocked = tuple(task_id for task_id, count in incoming.items() if count > 0)
    return DependencyOrder(tuple(ordered), blocked)


def validate_acyclic(graph: dict[UUID, set[UUID]]) -> tuple[UUID, ...]:
    result = order_dependency_graph(graph)

    if result.blocked:
        raise DependencyCycleError(result.blocked)

    return result.ordered


def validate_task_dependencies(
    tasks: Mapping[UUID, FlexibleTask],
    dependencies: Iterable[Dependency],
) -> tuple[FlexibleTask, ...]:
    graph = build_dependency_graph(tasks, dependencies)
    ordered_ids = validate_acyclic(graph)
    return tuple(tasks[task_id] for task_id in ordered_ids)
