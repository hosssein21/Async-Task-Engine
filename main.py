
from task_engine.engine import SequentialEngine
from task_engine.models import Job, JobPriority, TaskType

from tasks.cpu_tasks import calculate_statistics
from tasks.io_tasks import generate_report
from tasks.async_tasks import check_service


def main() -> None:
    engine = SequentialEngine()

    engine.register_handler(TaskType.CPU, calculate_statistics)
    engine.register_handler(TaskType.IO, generate_report)
    engine.register_handler(TaskType.ASYNC, check_service)

    engine.submit(
        Job(
            name="Generate monthly report",
            task_type=TaskType.IO,
            payload={"report_name": "monthly"},
            priority=JobPriority.NORMAL,
        )
    )

    engine.submit(
        Job(
            name="Calculate dataset statistics",
            task_type=TaskType.CPU,
            payload={"numbers": [10, 20, 30, 40, 50]},
            priority=JobPriority.HIGH,
        )
    )

    engine.submit(
        Job(
            name="Check payment service",
            task_type=TaskType.ASYNC,
            payload={"service_name": "payment-service"},
            priority=JobPriority.LOW,
        )
    )

    results = engine.run_all()

    for job in results:
        print(f"\nJob: {job.name}")
        print(f"Status: {job.status.value}")

        if job.status == job.status.COMPLETED:
            print(f"Result: {job.result}")
        else:
            print(f"Error: {job.error}")


if __name__ == "__main__":
    main()