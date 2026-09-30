
import unittest

from task_engine.models import Job, JobPriority, TaskType
from task_engine.scheduler import (
    DuplicateJobError,
    InvalidJobError,
    JobScheduler,
)


class JobSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.scheduler = JobScheduler()

    def make_job(self, name, priority=JobPriority.NORMAL):
        return Job(
            name=name,
            task_type=TaskType.IO,
            priority=priority,
        )

    def test_higher_priority_jobs_are_retrieved_first(self):
        low = self.make_job("low", JobPriority.LOW)
        high = self.make_job("high", JobPriority.HIGH)
        normal = self.make_job("normal", JobPriority.NORMAL)

        self.scheduler.submit(low)
        self.scheduler.submit(high)
        self.scheduler.submit(normal)

        self.assertEqual(self.scheduler.get_next().name, "high")
        self.assertEqual(self.scheduler.get_next().name, "normal")
        self.assertEqual(self.scheduler.get_next().name, "low")

    def test_equal_priorities_preserve_submission_order(self):
        first = self.make_job("first", JobPriority.HIGH)
        second = self.make_job("second", JobPriority.HIGH)

        self.scheduler.submit(first)
        self.scheduler.submit(second)

        self.assertEqual(self.scheduler.get_next().name, "first")
        self.assertEqual(self.scheduler.get_next().name, "second")

    def test_duplicate_submission_is_rejected(self):
        job = self.make_job("example")

        self.scheduler.submit(job)

        with self.assertRaises(DuplicateJobError):
            self.scheduler.submit(job)

    def test_non_pending_job_is_rejected(self):
        job = self.make_job("already running")
        job.start()

        with self.assertRaises(InvalidJobError):
            self.scheduler.submit(job)

    def test_peek_does_not_remove_job(self):
        job = self.make_job("example")
        self.scheduler.submit(job)

        self.assertIs(self.scheduler.peek(), job)
        self.assertEqual(self.scheduler.size(), 1)

    def test_empty_scheduler_raises_index_error(self):
        with self.assertRaises(IndexError):
            self.scheduler.get_next()

        with self.assertRaises(IndexError):
            self.scheduler.peek()


if __name__ == "__main__":
    unittest.main()