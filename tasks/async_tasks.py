
def check_service(payload: dict) -> dict:
    service_name = payload.get("service_name", "example-service")

    # Simulate a successful service check.
    return {
        "service": service_name,
        "available": True,
    }