
import heapq
from itertools import count

from task_engine.models import Job, JobStatus


class DuplicateJobError(ValueError):
    """Raised when a job ID has already been submitted."""


class InvalidJobError(ValueError):
    """Raised when a job cannot be accepted by the scheduler."""


class JobScheduler:
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, Job]] = []
        self._sequence = count()
        self._known_job_ids: set = set()

    def submit(self, job: Job) -> None:
        if job.id in self._known_job_ids:
            raise DuplicateJobError(
                f"Job {job.id} has already been submitted"
            )

        if job.status != JobStatus.PENDING:
            raise InvalidJobError(
                f"Cannot submit job in state: {job.status.value}"
            )

        entry = (
            int(job.priority),
            next(self._sequence),
            job,
        )

        heapq.heappush(self._heap, entry)
        self._known_job_ids.add(job.id)

    def get_next(self) -> Job:
        if self.is_empty():
            raise IndexError("Cannot retrieve from an empty scheduler")

        _, _, job = heapq.heappop(self._heap)
        return job

    def peek(self) -> Job:
        if self.is_empty():
            raise IndexError("Cannot peek into an empty scheduler")

        return self._heap[0][2]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)