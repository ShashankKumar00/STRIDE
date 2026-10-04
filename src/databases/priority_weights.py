# Priority Weight System for STRIDE
# Implements priority-to-weight mapping and vector normalization (Phase 3 & 5)

PRIORITY_WEIGHTS = {
    "Very High": 5.0,
    "High": 4.0,
    "Medium": 3.0,
    "Low": 2.0,
    "Very Low": 1.0
}


def generate_weights(priority_selections):
    """
    Converts user priority selections into numerical weights.
    
    Args:
        priority_selections (dict): Mapping of parameter name to priority string.
                                    e.g. {"Payload": "High", "Terrain": "Medium"}
                                    
    Returns:
        dict: Mapping of parameter name to numerical weight (1.0 to 5.0).
    """
    weights = {}
    for parameter, priority in priority_selections.items():
        weights[parameter] = PRIORITY_WEIGHTS.get(priority, 3.0)
    return weights


def normalize_weights(weights):
    """
    Normalizes a dictionary of weights so that their sum equals 1.0.
    
    Args:
        weights (dict): Mapping of parameter name to numeric weight.
        
    Returns:
        dict: Mapping of parameter name to normalized weight where sum(weights.values()) == 1.0.
    """
    total = sum(weights.values())
    if total <= 0:
        count = len(weights)
        return {k: (1.0 / count) if count > 0 else 0.0 for k in weights}
    return {k: (v / total) for k, v in weights.items()}