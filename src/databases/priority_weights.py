# Priority Weight System for STRIDE


PRIORITY_WEIGHTS = {
    "Very High": 5,
    "High": 4,
    "Medium": 3,
    "Low": 2,
    "Very Low": 1
}


def generate_weights(priority_selections):
    """
    Converts the user's priority selections into numerical weights.

    Example:
        "High" -> 4
        "Medium" -> 3
    """

    weights = {}

    for parameter, priority in priority_selections.items():

        weights[parameter] = PRIORITY_WEIGHTS.get(
            priority,
            3
        )

    return weights