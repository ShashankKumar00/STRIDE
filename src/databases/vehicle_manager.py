import os
import json
import copy
from typing import List, Dict, Any, Tuple

from databases.vehicle_database import VEHICLE_DATABASE

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
CUSTOM_VEHICLES_FILE = os.path.join(DATA_DIR, "custom_vehicles.json")


def load_custom_vehicles() -> List[Dict[str, Any]]:
    """Loads user/company added custom vehicles from JSON storage."""
    if not os.path.exists(CUSTOM_VEHICLES_FILE):
        return []
    try:
        with open(CUSTOM_VEHICLES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        print(f"[VehicleManager] Error loading custom vehicles: {e}")
        return []


def save_all_custom_vehicles(vehicles: List[Dict[str, Any]]) -> bool:
    """Persists the full custom vehicles list to JSON storage."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(CUSTOM_VEHICLES_FILE, "w", encoding="utf-8") as f:
            json.dump(vehicles, f, indent=4)
        return True
    except Exception as e:
        print(f"[VehicleManager] Error saving custom vehicles: {e}")
        return False


def validate_vehicle_input(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates that a new vehicle candidate complies with the canonical schema.
    Returns (is_valid, error_message).
    """
    if not data.get("vehicle_name", "").strip():
        return False, "Vehicle Name is mandatory."
    if not data.get("manufacturer", "").strip():
        return False, "Manufacturer / Developer is mandatory."
    if not data.get("mobility_type", "").strip():
        return False, "Mobility Type is mandatory."
    if not data.get("mission_roles") or len(data.get("mission_roles", [])) == 0:
        return False, "At least one Mission Role must be selected."
    if not data.get("terrain_capabilities") or len(data.get("terrain_capabilities", [])) == 0:
        return False, "At least one Terrain Capability must be selected."

    # Validate numerical fields (allow None, but if present must be positive float)
    num_fields = ["payload_capacity_kg", "max_speed_kmh", "operating_range_km", "endurance_hours", "max_control_range_km"]
    for field in num_fields:
        val = data.get(field)
        if val is not None and val != "":
            try:
                f_val = float(val)
                if f_val <= 0:
                    return False, f"{field.replace('_', ' ').title()} must be strictly greater than 0."
            except (ValueError, TypeError):
                return False, f"{field.replace('_', ' ').title()} must be a valid number or empty (Unknown)."

    return True, ""


def add_vehicle(raw_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Sanitizes, assigns a unique ID, persists, and returns the added vehicle.
    Returns (success, message, vehicle_dict).
    """
    is_valid, err = validate_vehicle_input(raw_data)
    if not is_valid:
        return False, err, {}

    custom_vehicles = load_custom_vehicles()
    
    # Check for duplicate names across base + custom
    all_names = [v["vehicle_name"].lower() for v in get_active_catalog()]
    if raw_data["vehicle_name"].strip().lower() in all_names:
        return False, f"A vehicle named '{raw_data['vehicle_name'].strip()}' already exists in the system.", {}

    # Generate sequential unique ID
    next_index = len(custom_vehicles) + 1
    new_id = f"UGV-OEM-{next_index:03d}"

    def parse_float_or_none(v):
        if v is None or v == "":
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    # Construct clean schema record
    clean_vehicle = {
        "vehicle_id": new_id,
        "vehicle_name": raw_data["vehicle_name"].strip(),
        "manufacturer": raw_data["manufacturer"].strip(),
        "mobility_type": raw_data["mobility_type"].strip(),
        "mission_roles": list(raw_data.get("mission_roles", [])),
        "terrain_capabilities": list(raw_data.get("terrain_capabilities", [])),
        "payload_capacity_kg": parse_float_or_none(raw_data.get("payload_capacity_kg")),
        "max_speed_kmh": parse_float_or_none(raw_data.get("max_speed_kmh")) or 15.0,
        "operating_range_km": parse_float_or_none(raw_data.get("operating_range_km")),
        "endurance_hours": parse_float_or_none(raw_data.get("endurance_hours")),
        "max_control_range_km": parse_float_or_none(raw_data.get("max_control_range_km")),
        "control_link_types": list(raw_data.get("control_link_types", ["COFDM NLOS (Non-Line of Sight Mesh)"])),
        "climate_altitude": {
            "min_operating_temp_c": parse_float_or_none(raw_data.get("min_operating_temp_c")) or -20.0,
            "max_operating_temp_c": parse_float_or_none(raw_data.get("max_operating_temp_c")) or 50.0,
            "max_altitude_m_asl": int(raw_data.get("max_altitude_m_asl", 4000) or 4000),
            "cold_start_capable": bool(raw_data.get("cold_start_capable", True))
        },
        "stealth_profile": {
            "propulsion_type": raw_data.get("propulsion_type", "All-Electric (Silent)"),
            "acoustic_stealth_db_at_10m": parse_float_or_none(raw_data.get("acoustic_stealth_db_at_10m")) or 45.0,
            "thermal_signature_level": raw_data.get("thermal_signature_level", "Low")
        },
        "status": raw_data.get("status", "Developed / Demonstrated").strip(),
        "source": raw_data.get("source", "User / Defence OEM Ingestion").strip(),
        "image_path": raw_data.get("image_path", "assets/images/kalyani_ecars_4x4.jpg").strip(),
        "provenance": {
            "payload_capacity": "OEM-reported" if raw_data.get("payload_capacity_kg") else "Unknown",
            "max_speed": "OEM-reported",
            "operating_range": "OEM-reported" if raw_data.get("operating_range_km") else "Unknown",
            "endurance": "OEM-reported" if raw_data.get("endurance_hours") else "Unknown",
            "control_range": "OEM-reported",
            "climate_altitude": "OEM-specified",
            "stealth": "OEM-specified"
        }
    }

    custom_vehicles.append(clean_vehicle)
    if save_all_custom_vehicles(custom_vehicles):
        return True, f"Vehicle '{clean_vehicle['vehicle_name']}' successfully registered with ID {new_id}!", clean_vehicle
    else:
        return False, "Failed to persist new vehicle to storage.", {}


def get_active_catalog() -> List[Dict[str, Any]]:
    """Returns the combined catalog of base 24 platforms + any custom added platforms."""
    base = copy.deepcopy(VEHICLE_DATABASE)
    custom = load_custom_vehicles()
    return base + custom


def reset_custom_vehicles() -> bool:
    """Clears all user-added custom vehicles."""
    return save_all_custom_vehicles([])
