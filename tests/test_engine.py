
import unittest

from task_engine.engine import SequentialEngine
from task_engine.models import Job, JobStatus, TaskType


class SequentialEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = SequentialEngine()
        self.engine.register_handler(
            TaskType.CPU,
            lambda payload: payload["value"] * 2,
        )

    def test_successful_job(self):
        job = Job(
            name="Double a number",
            task_type=TaskType.CPU,
            payload={"value": 21},
        )

        self.engine.submit(job)
        results = self.engine.run_all()

        self.assertEqual(len(results), 1)
        self.assertEqual(job.status, JobStatus.COMPLETED)
        self.assertEqual(job.result, 42)

    def test_handler_failure_does_not_crash_engine(self):
        def failing_handler(payload):
            raise ValueError("Something went wrong")

        engine = SequentialEngine()
        engine.register_handler(TaskType.CPU, failing_handler)

        job = Job(name="Failing job", task_type=TaskType.CPU)
        engine.submit(job)

        result = engine.run_next()

        self.assertEqual(result.status, JobStatus.FAILED)
        self.assertIn("Something went wrong", result.error)

    def test_missing_handler_is_rejected(self):
        job = Job(name="Unknown handler", task_type=TaskType.IO)

        with self.assertRaises(ValueError):
            self.engine.submit(job)

    def test_empty_engine_returns_no_job(self):
        self.assertIsNone(self.engine.run_next())
        self.assertEqual(self.engine.run_all(), [])


if __name__ == "__main__":
    unittest.main()