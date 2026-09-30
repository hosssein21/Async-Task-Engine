
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(str, Enum):
    IO = "io"
    CPU = "cpu"
    ASYNC = "async"


class JobPriority(int, Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Job:
    name: str
    task_type: TaskType
    payload: dict[str, Any] = field(default_factory=dict)
    priority: JobPriority = JobPriority.NORMAL

    id: UUID = field(default_factory=uuid4, init=False)
    status: JobStatus = field(
        default=JobStatus.PENDING,
        init=False,
    )
    created_at: datetime = field(
        default_factory=utc_now,
        init=False,
    )
    started_at: datetime | None = field(default=None, init=False)
    finished_at: datetime | None = field(default=None, init=False)
    result: Any = field(default=None, init=False)
    error: str | None = field(default=None, init=False)

    def start(self) -> None:
        if self.status != JobStatus.PENDING:
            raise ValueError(
                f"Cannot start job in state: {self.status.value}"
            )

        self.status = JobStatus.RUNNING
        self.started_at = utc_now()

    def complete(self, result: Any = None) -> None:
        if self.status != JobStatus.RUNNING:
            raise ValueError(
                f"Cannot complete job in state: {self.status.value}"
            )

        self.status = JobStatus.COMPLETED
        self.result = result
        self.finished_at = utc_now()

    def fail(self, error: str) -> None:
        if self.status != JobStatus.RUNNING:
            raise ValueError(
                f"Cannot fail job in state: {self.status.value}"
            )

        self.status = JobStatus.FAILED
        self.error = error
        self.finished_at = utc_now()