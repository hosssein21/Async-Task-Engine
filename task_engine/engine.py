
from collections.abc import Callable
from typing import Any

from task_engine.models import Job, JobStatus, TaskType
from task_engine.scheduler import JobScheduler


Handler = Callable[[dict[str, Any]], Any]


class SequentialEngine:
    def __init__(self) -> None:
        self.scheduler = JobScheduler()
        self._handlers: dict[TaskType, Handler] = {}

    def register_handler(
        self,
        task_type: TaskType,
        handler: Handler,
    ) -> None:
        if task_type in self._handlers:
            raise ValueError(
                f"Handler already registered for {task_type.value}"
            )

        self._handlers[task_type] = handler

    def submit(self, job: Job) -> None:
        if job.task_type not in self._handlers:
            raise ValueError(
                f"No handler registered for {job.task_type.value}"
            )

        self.scheduler.submit(job)

    def run_next(self) -> Job | None:
        if self.scheduler.is_empty():
            return None

        job = self.scheduler.get_next()
        job.start()

        try:
            handler = self._handlers[job.task_type]
            result = handler(job.payload)
            job.complete(result)
        except Exception as exc:
            job.fail(f"{type(exc).__name__}: {exc}")

        return job

    def run_all(self) -> list[Job]:
        completed_run: list[Job] = []

        while not self.scheduler.is_empty():
            job = self.run_next()

            if job is not None:
                completed_run.append(job)

        return completed_run