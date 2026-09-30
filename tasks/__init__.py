
def calculate_statistics(payload: dict) -> dict:
    numbers = payload.get("numbers", [])

    if not numbers:
        raise ValueError("The numbers list cannot be empty")

    return {
        "count": len(numbers),
        "total": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "minimum": min(numbers),
        "maximum": max(numbers),
    }