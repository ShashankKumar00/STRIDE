import re
from typing import Dict, Any, List


ROLE_KEYWORDS = {
    "Surveillance": ["surveillance", "watch", "monitoring", "observe", "observation", "perimeter", "sentry"],
    "Reconnaissance": ["recon", "reconnaissance", "scout", "scouting", "patrol", "pathfinding", "probe"],
    "Mine Detection / Clearance": ["mine", "demining", "minefield", "counter-mine", "breach", "breaching", "gpr"],
    "CBRN Reconnaissance": ["cbrn", "chemical", "biological", "radiological", "nuclear", "hazmat", "toxic", "radiation"],
    "Combat / Tactical Support": ["combat", "tactical support", "fire support", "rcws", "weapon", "turret", "engage", "assault"],
    "Logistics / Transport / Casualty Evacuation": ["logistics", "supply", "supplies", "mule", "ammo", "ammunition", "transport", "cargo", "casevac", "casualty", "stretcher", "evacuation"],
    "EOD / IED Disposal": ["eod", "ied", "bomb", "disposal", "defusal", "disruptor", "explosive", "suspicious package"],
    "High-Altitude Logistics / Extreme Cold": ["high altitude", "ladakh", "siachen", "glacier", "extreme cold", "sub-zero", "subzero", "himalayan"],
    "Precision Strike / Anti-Armor": ["strike", "precision strike", "anti-tank", "atgm", "anti-armor", "bunker buster", "kamikaze", "kinetic"],
    "Urban Assault / Confined Space Recon": ["urban assault", "confined space", "indoor", "room", "building", "train", "aircraft", "corridor", "stair"]
}

TERRAIN_KEYWORDS = {
    "Desert / Sand": ["desert", "sand", "dunes", "thar", "rajasthan", "arid"],
    "Snow / Ice": ["snow", "ice", "glacier", "siachen", "frozen", "winter", "blizzard"],
    "Rugged / Mountainous / Rocky": ["mountain", "mountains", "mountainous", "rocky", "rugged", "hills", "incline", "steep", "ladakh", "pass", "boulders"],
    "Mud / Soft Ground": ["mud", "muddy", "soft ground", "marsh", "swamp", "bog", "wetland"],
    "Paved Road / Urban": ["paved", "road", "urban", "asphalt", "highway", "city", "streets"],
    "Plain / Grassland": ["plain", "plains", "grassland", "flat", "prairie", "open terrain"],
    "Extreme Obstacles / Stairs / Confined Spaces": ["stairs", "stair", "confined", "rubble", "doorway", "aisle", "interior", "corridor"],
    "Amphibious / Riverine / Fording": ["amphibious", "river", "riverine", "fording", "water crossing", "stream", "lake", "swampy"]
}


def parse_mission_narrative(text: str) -> Dict[str, Any]:
    """
    Parses natural language free-text mission descriptions and extracts structured
    mission parameters for the STRIDE decision engine.
    """
    text_lower = text.lower()
    
    extracted = {
        "roles": [],
        "terrain": "Plain / Grassland",
        "payload_kg": 50.0,
        "operating_range_km": 15.0,
        "min_time_hours": 1.0,
        "max_time_hours": 3.0,
        "standoff_km": 5.0,
        "control_link": "COFDM NLOS (Non-Line of Sight Mesh)",
        "altitude_m": 1500,
        "temperature_c": 25.0,
        "stealth_required": False,
        "confidence_log": []
    }
    
    # 1. Match Roles
    matched_roles = []
    for role, kw_list in ROLE_KEYWORDS.items():
        for kw in kw_list:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                if role not in matched_roles:
                    matched_roles.append(role)
                    extracted["confidence_log"].append(f"Detected Mission Role '{role}' via keyword '{kw}'")
                break
    if matched_roles:
        extracted["roles"] = matched_roles
    else:
        extracted["roles"] = ["Surveillance"]
        
    # 2. Match Terrain
    matched_terrain = None
    for terrain, kw_list in TERRAIN_KEYWORDS.items():
        for kw in kw_list:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                matched_terrain = terrain
                extracted["confidence_log"].append(f"Detected Terrain '{terrain}' via keyword '{kw}'")
                break
        if matched_terrain:
            break
    if matched_terrain:
        extracted["terrain"] = matched_terrain

    # 3. Match Payload
    # e.g., "50 kg", "200 kilograms", "half ton", "1 ton", "750kg"
    payload_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kilos|kilogram|kilograms)', text_lower)
    if payload_match:
        extracted["payload_kg"] = float(payload_match.group(1))
        extracted["confidence_log"].append(f"Extracted payload: {extracted['payload_kg']} kg")
    elif "half ton" in text_lower or "500 kg" in text_lower:
        extracted["payload_kg"] = 500.0
    elif "1 ton" in text_lower or "1000 kg" in text_lower or "one ton" in text_lower:
        extracted["payload_kg"] = 1000.0

    # 4. Match Mission Distance / Range
    # e.g. "15 km", "20 kilometers", "10km", "5 miles"
    dist_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kms|kilometer|kilometers)', text_lower)
    if dist_match:
        extracted["operating_range_km"] = float(dist_match.group(1))
        extracted["confidence_log"].append(f"Extracted mission distance: {extracted['operating_range_km']} km")

    # 5. Match Standoff / Control Range
    standoff_match = re.search(r'(?:standoff|stand-off|control range|remote range|from)\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*(?:km|kilometer)', text_lower)
    if standoff_match:
        extracted["standoff_km"] = float(standoff_match.group(1))
        extracted["confidence_log"].append(f"Extracted operator standoff distance: {extracted['standoff_km']} km")

    # 6. Match Altitude
    # e.g. "15000 ft", "16,000 feet", "4500 m", "5000 meters"
    alt_ft_match = re.search(r'(\d+(?:,\d+)?)\s*(?:ft|feet)', text_lower)
    alt_m_match = re.search(r'(\d+(?:,\d+)?)\s*(?:m|meter|meters)\s+(?:asl|altitude)?', text_lower)
    if alt_ft_match:
        feet = float(alt_ft_match.group(1).replace(",", ""))
        extracted["altitude_m"] = int(feet * 0.3048)
        extracted["confidence_log"].append(f"Extracted altitude: {feet} ft (~{extracted['altitude_m']} m ASL)")
    elif alt_m_match:
        extracted["altitude_m"] = int(alt_m_match.group(1).replace(",", ""))
        extracted["confidence_log"].append(f"Extracted altitude: {extracted['altitude_m']} m ASL")
    elif "siachen" in text_lower or "high altitude" in text_lower:
        extracted["altitude_m"] = 5200
        extracted["confidence_log"].append("Inferred high altitude: 5200 m ASL (Siachen/Ladakh context)")

    # 7. Match Temperature / Climate
    temp_match = re.search(r'(-?\d+(?:\.\d+)?)\s*(?:°c|c|deg c|degrees)', text_lower)
    if temp_match:
        extracted["temperature_c"] = float(temp_match.group(1))
        extracted["confidence_log"].append(f"Extracted temperature: {extracted['temperature_c']}°C")
    elif "sub-zero" in text_lower or "subzero" in text_lower or "freezing" in text_lower:
        extracted["temperature_c"] = -20.0
        extracted["confidence_log"].append("Inferred sub-zero operating temperature: -20°C")
    elif "desert heat" in text_lower or "summer" in text_lower:
        extracted["temperature_c"] = 48.0
        extracted["confidence_log"].append("Inferred high desert temperature: +48°C")

    # 8. Match Stealth
    if any(k in text_lower for k in ["silent", "stealth", "quiet", "low acoustic", "covert", "whisper"]):
        extracted["stealth_required"] = True
        extracted["confidence_log"].append("Identified strict stealth requirement (Silent Electric)")

    # 9. Match Time Window
    # e.g., "within 2 hours", "1.5h to 3h", "90 minutes", "deadline of 4 hours"
    time_range_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:h|hr|hours)?\s*(?:to|-)\s*(\d+(?:\.\d+)?)\s*(?:h|hr|hours)', text_lower)
    time_single_match = re.search(r'(?:within|in|deadline)\s*(\d+(?:\.\d+)?)\s*(?:h|hr|hours)', text_lower)
    time_min_match = re.search(r'(\d+)\s*(?:min|mins|minutes)', text_lower)
    
    if time_range_match:
        extracted["min_time_hours"] = float(time_range_match.group(1))
        extracted["max_time_hours"] = float(time_range_match.group(2))
        extracted["confidence_log"].append(f"Extracted time window: {extracted['min_time_hours']}h to {extracted['max_time_hours']}h")
    elif time_single_match:
        extracted["max_time_hours"] = float(time_single_match.group(1))
        extracted["min_time_hours"] = max(0.5, extracted["max_time_hours"] * 0.5)
        extracted["confidence_log"].append(f"Extracted deadline: {extracted['max_time_hours']}h")
    elif time_min_match:
        minutes = float(time_min_match.group(1))
        extracted["max_time_hours"] = round(minutes / 60.0, 2)
        extracted["min_time_hours"] = max(0.25, round(extracted["max_time_hours"] * 0.5, 2))
        extracted["confidence_log"].append(f"Extracted time window from minutes: {extracted['max_time_hours']}h deadline")

    # 10. Match Jam-Proof / Fiber Optic
    if any(k in text_lower for k in ["jamming", "ew", "electronic warfare", "fiber", "fiber-optic", "jam-proof"]):
        extracted["control_link"] = "Fiber-Optic (Jam-Proof / EW-Immune)"
        extracted["confidence_log"].append("Identified EW-saturated environment: Fiber-Optic link requested")
    elif any(k in text_lower for k in ["drone relay", "satellite", "satcom", "blos"]):
        extracted["control_link"] = "SATCOM / BLOS Drone Relay"
        extracted["confidence_log"].append("Identified Beyond-Line-of-Sight link: SATCOM / Drone Relay requested")

    return extracted
