
from task_engine.models import Job, TaskType, JobPriority
from task_engine.scheduler import JobScheduler


def main() -> None:
    scheduler = JobScheduler()

    jobs = [
        Job(
            name="Generate report",
            task_type=TaskType.IO,
            priority=JobPriority.NORMAL,
        ),
        Job(
            name="Process dataset",
            task_type=TaskType.CPU,
            priority=JobPriority.LOW,
        ),
        Job(
            name="Send alert",
            task_type=TaskType.ASYNC,
            priority=JobPriority.HIGH,
        ),
        Job(
            name="Check service",
            task_type=TaskType.IO,
            priority=JobPriority.HIGH,
        ),
    ]

    for job in jobs:
        scheduler.submit(job)

    print(f"Jobs waiting: {scheduler.size()}")
    print(f"Next job: {scheduler.peek().name}")

    print("\nExecution order:")

    while not scheduler.is_empty():
        job = scheduler.get_next()
        print(f"{job.priority.name}: {job.name}")

    print(f"\nJobs waiting: {scheduler.size()}")


if __name__ == "__main__":
    main()