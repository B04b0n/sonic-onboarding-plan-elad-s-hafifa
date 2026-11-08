events = [
    {"id": 1, "status": "ok", "latency_ms": 120},
    {"id": 2, "status": "error", "latency_ms": 900},
    {"id": 3, "status": "ok", "latency_ms": 450},
    {"id": 4, "status": "ok", "latency_ms": 200},
    {"id": 5, "status": "error", "latency_ms": 1100},
]


def error_count():
    errors_amount = 0

    for event in events:
        if event["status"] == "error":
            errors_amount +=1

    return errors_amount

def avg_latency(list):
    """
    Args:
        list: list of events

    Returns: latency average over all events
    """
    laten_sum = 0
    for event in list:
        laten_sum += event["latency_ms"]

    return laten_sum/len(list)

def get_slow_events(events_list, threshold):
    """

    Args:
        events_list:
        threshold:

    Returns:

    """
    slow_events = []

    for event in events_list:
        if event["latency_ms"] < threshold:
            slow_events.append(event)

    return slow_events


print('asdada')