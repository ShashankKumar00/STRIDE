PRIORITY_POINTS = {
    "Very High": 6,
    "High": 5,
    "Medium": 4,
    "Low": 2,
    "Very Low": 1
}


def generate_weights(priority_order):
    total_points = sum(
        PRIORITY_POINTS[priority]
        for priority in priority_order.values()
    )

    weights = {}

    for parameter, priority in priority_order.items():
        points = PRIORITY_POINTS[priority]
        weights[parameter] = (points / total_points) * 100

    return weights