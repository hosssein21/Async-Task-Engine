
from task_engine.models import Job, TaskType, JobPriority


def main() -> None:
    job = Job(
        name="Calculate dataset statistics",
        task_type=TaskType.CPU,
        payload={"numbers": [10, 20, 30, 40, 50]},
        priority=JobPriority.HIGH,
    )

    print(f"ID: {job.id}")
    print(f"Name: {job.name}")
    print(f"Status: {job.status.value}")

    job.start()
    print(f"After starting: {job.status.value}")

    result = {"average": 30}
    job.complete(result)

    print(f"After completion: {job.status.value}")
    print(f"Result: {job.result}")
    print(f"Created at: {job.created_at}")
    print(f"Started at: {job.started_at}")
    print(f"Finished at: {job.finished_at}")


if __name__ == "__main__":
    main()