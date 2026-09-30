
import time


def generate_report(payload: dict) -> dict:
    report_name = payload.get("report_name", "default")

    # Simulate blocking I/O.
    time.sleep(0.5)

    return {
        "report_name": report_name,
        "status": "generated",
    }