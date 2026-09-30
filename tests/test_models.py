
import unittest

from task_engine.models import Job, JobStatus, TaskType


class JobModelTests(unittest.TestCase):
    def test_job_starts_as_pending(self):
        job = Job(
            name="Example job",
            task_type=TaskType.IO,
        )

        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertIsNone(job.started_at)

    def test_job_completes_successfully(self):
        job = Job(
            name="Example job",
            task_type=TaskType.CPU,
        )

        job.start()
        job.complete(result=42)

        self.assertEqual(job.status, JobStatus.COMPLETED)
        self.assertEqual(job.result, 42)
        self.assertIsNotNone(job.finished_at)

    def test_cannot_complete_pending_job(self):
        job = Job(
            name="Example job",
            task_type=TaskType.ASYNC,
        )

        with self.assertRaises(ValueError):
            job.complete(result=42)

    def test_cannot_start_job_twice(self):
        job = Job(
            name="Example job",
            task_type=TaskType.IO,
        )

        job.start()

        with self.assertRaises(ValueError):
            job.start()


if __name__ == "__main__":
    unittest.main()