# Scoring Engine for STRIDE

def score_requirement(vehicle_value, required_value):
    if required_value <= 0:
        return 0
    try:
        vehicle_value = float(vehicle_value)
        required_value = float(required_value)
    except (ValueError, TypeError):
        return 0
    score = (vehicle_value / required_value) * 100
    return min(score, 100)

def score_terrain(vehicle_terrain, required_terrain):
    if not vehicle_terrain:
        return 0
    if isinstance(vehicle_terrain, list):
        return 100 if required_terrain in vehicle_terrain else 0
    return 100 if required_terrain == vehicle_terrain else 0

def score_mission_role(vehicle, required_role):
    supported_roles = vehicle.get("mission_roles", [])
    if isinstance(supported_roles, list) and required_role in supported_roles:
        return 100
    return 0

def score_mission_time(mission_distance, vehicle_speed, minimum_time, maximum_time):
    if (
        mission_distance <= 0
        or vehicle_speed <= 0
        or minimum_time <= 0
        or maximum_time <= 0
    ):
        return 0

    estimated_time = mission_distance / vehicle_speed

    if minimum_time <= estimated_time <= maximum_time:
        return 100

    if estimated_time > maximum_time:
        excess_time = estimated_time - maximum_time
        score = (maximum_time / (maximum_time + excess_time)) * 100
        return max(0, min(score, 100))

    if estimated_time < minimum_time:
        difference = minimum_time - estimated_time
        score = (minimum_time / (minimum_time + difference)) * 100
        return max(0, min(score, 100))

    return 0

def calculate_required_speed(mission_distance, maximum_time):
    if mission_distance <= 0 or maximum_time <= 0:
        return 0
    return mission_distance / maximum_time

def score_speed(vehicle_speed, required_speed):
    if required_speed <= 0:
        return 0
    try:
        vehicle_speed = float(vehicle_speed)
    except (ValueError, TypeError):
        return 0
    score = (vehicle_speed / required_speed) * 100
    return min(score, 100)

def calculate_vehicle_score(vehicle, requirements, weights):
    scores = {}

    scores["Mission Role"] = score_mission_role(
        vehicle,
        requirements.get("Mission Role", "")
    )

    scores["Terrain"] = score_terrain(
        vehicle.get("terrain", []),
        requirements.get("Terrain", "")
    )

    scores["Payload"] = score_requirement(
        vehicle.get("payload_capacity", vehicle.get("payload", 0)),
        requirements.get("Payload", 0)
    )

    scores["Operating Range"] = score_requirement(
        vehicle.get("operating_range", vehicle.get("range", 0)),
        requirements.get("Operating Range", 0)
    )

    vehicle_speed = vehicle.get("max_speed", vehicle.get("speed", 0))

    scores["Minimum Mission Time"] = score_mission_time(
        requirements.get("Operating Range", 0),
        vehicle_speed,
        requirements.get("Minimum Mission Time", 0),
        requirements.get("Maximum Mission Time", 0)
    )
    scores["Maximum Mission Time"] = scores["Minimum Mission Time"]

    required_speed = calculate_required_speed(
        requirements.get("Operating Range", 0),
        requirements.get("Maximum Mission Time", 0)
    )
    scores["Internal Speed"] = score_speed(
        vehicle_speed,
        required_speed
    )

    scores["Endurance Check"] = score_requirement(
        vehicle.get("endurance", 0),
        requirements.get("Endurance", 0)
    )

    weighted_score = 0
    total_weight = 0

    for parameter in ["Mission Role", "Terrain", "Payload", "Operating Range"]:
        weight = weights.get(parameter, 0)
        weighted_score += scores[parameter] * weight
        total_weight += weight

    min_time_weight = weights.get("Minimum Mission Time", 0)
    max_time_weight = weights.get("Maximum Mission Time", 0)
    mission_time_weight = min_time_weight + max_time_weight

    weighted_score += scores["Minimum Mission Time"] * mission_time_weight
    total_weight += mission_time_weight

    speed_weight = max_time_weight
    endurance_weight = weights.get("Endurance", 0)

    weighted_score += scores["Internal Speed"] * speed_weight
    weighted_score += scores["Endurance Check"] * endurance_weight

    total_weight += speed_weight
    total_weight += endurance_weight

    final_score = (weighted_score / total_weight) if total_weight > 0 else 0
    return final_score, scores

def rank_vehicles(vehicles, requirements, weights):
    results = []
    if not isinstance(vehicles, list):
        return results

    for vehicle in vehicles:
        final_score, scores = calculate_vehicle_score(
            vehicle,
            requirements,
            weights
        )
        results.append({
            "vehicle_id": vehicle.get("vehicle_id", "N/A"),
            "vehicle_name": vehicle.get("vehicle_name", "Unknown Vehicle"),
            "final_score": final_score,
            "scores": scores
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results