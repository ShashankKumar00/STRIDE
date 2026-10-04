# Standardized Vehicle Database for STRIDE
# Conforms to Phase 4 DATA_SCHEMA.md

VEHICLE_DATABASE = [
    {
        "vehicle_id": "UGV-IND-001",
        "vehicle_name": "MUNTRA-S",
        "manufacturer": "DRDO - CVRDE",
        "mobility_type": "Tracked",
        "mission_roles": ["Surveillance", "Reconnaissance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": None,
        "max_speed_kmh": 20.0,
        "operating_range_km": 20.0,
        "endurance_hours": 8.0,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    },
    {
        "vehicle_id": "UGV-IND-002",
        "vehicle_name": "MUNTRA-M",
        "manufacturer": "DRDO - CVRDE",
        "mobility_type": "Tracked",
        "mission_roles": ["Mine Detection / Clearance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": None,
        "max_speed_kmh": 20.0,
        "operating_range_km": 20.0,
        "endurance_hours": 8.0,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    },
    {
        "vehicle_id": "UGV-IND-003",
        "vehicle_name": "MUNTRA-N",
        "manufacturer": "DRDO - CVRDE",
        "mobility_type": "Tracked",
        "mission_roles": ["CBRN Reconnaissance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": None,
        "max_speed_kmh": 20.0,
        "operating_range_km": 20.0,
        "endurance_hours": 8.0,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    },
    {
        "vehicle_id": "UGV-IND-004",
        "vehicle_name": "ECARS 4x4",
        "manufacturer": "Kalyani Strategic Systems / Bharat Forge",
        "mobility_type": "Wheeled 4x4",
        "mission_roles": [
            "Surveillance",
            "Combat / Tactical Support",
            "Logistics / Transport / Casualty Evacuation"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground"
        ],
        "payload_capacity_kg": 350.0,
        "max_speed_kmh": 20.0,
        "operating_range_km": None,
        "endurance_hours": None,
        "status": "Developed / Demonstrated",
        "source": "Bharat Forge - ECARS Brief",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Unknown",
            "endurance": "Unknown"
        }
    },
    {
        "vehicle_id": "UGV-IND-005",
        "vehicle_name": "Mooshak",
        "manufacturer": "Dronobotics",
        "mobility_type": "Tracked",
        "mission_roles": ["Surveillance", "Combat / Tactical Support"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 3.0,
        "max_speed_kmh": 20.0,
        "operating_range_km": 11.0,
        "endurance_hours": 8.0,
        "status": "Developed",
        "source": "Dronobotics - Mooshak UGV Specification",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    },
    {
        "vehicle_id": "UGV-IND-006",
        "vehicle_name": "BRUTE",
        "manufacturer": "Gridbots Technologies",
        "mobility_type": "Wheeled 6x6",
        "mission_roles": ["Combat / Tactical Support", "Surveillance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 50.0,
        "max_speed_kmh": 10.0,
        "operating_range_km": 20.0,
        "endurance_hours": None,
        "status": "Developed",
        "source": "Gridbots - BRUTE Combat UGV",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Unknown"
        }
    },
    {
        "vehicle_id": "UGV-IND-007",
        "vehicle_name": "HAWK",
        "manufacturer": "Gridbots Technologies",
        "mobility_type": "Tracked",
        "mission_roles": ["EOD / IED Disposal", "Reconnaissance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 100.0,
        "max_speed_kmh": 10.0,
        "operating_range_km": None,
        "endurance_hours": None,
        "status": "Developed",
        "source": "Gridbots - HAWK EOD Robot",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Unknown",
            "endurance": "Unknown"
        }
    },
    {
        "vehicle_id": "UGV-IND-008",
        "vehicle_name": "ZEUS",
        "manufacturer": "Gridbots Technologies",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Combat / Tactical Support",
            "Logistics / Transport / Casualty Evacuation",
            "Mine Detection / Clearance",
            "Surveillance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 1500.0,
        "max_speed_kmh": 15.0,
        "operating_range_km": 20.0,
        "endurance_hours": 12.0,
        "status": "Developed",
        "source": "Gridbots - ZEUS Heavy Combat UGV",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    },
    {
        "vehicle_id": "UGV-IND-009",
        "vehicle_name": "Vrishabh",
        "manufacturer": "Bhairav Robotics",
        "mobility_type": "Wheeled 4x4",
        "mission_roles": [
            "Combat / Tactical Support",
            "Surveillance",
            "Logistics / Transport / Casualty Evacuation",
            "Reconnaissance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 150.0,
        "max_speed_kmh": 50.0,
        "operating_range_km": 100.0,
        "endurance_hours": None,
        "status": "Under Development / Trials",
        "source": "Janes Defence - Bhairav Robotics Vrishabh",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Unknown"
        }
    },
    {
        "vehicle_id": "UGV-IND-010",
        "vehicle_name": "Daksh Scout",
        "manufacturer": "DRDO",
        "mobility_type": "Tracked",
        "mission_roles": ["Reconnaissance", "Surveillance"],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": None,
        "max_speed_kmh": 1.2,
        "operating_range_km": 0.2,
        "endurance_hours": 2.0,
        "status": "Developed",
        "source": "DRDO - Daksh Scout Technical Specification",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported"
        }
    }
]

# Backward compatibility alias
vehicle_database = VEHICLE_DATABASE


def get_all_vehicles():
    """Returns a copy of the canonical vehicle database."""
    return list(VEHICLE_DATABASE)


def display_all_vehicles():
    for v in VEHICLE_DATABASE:
        payload_str = f"{v['payload_capacity_kg']} kg" if v['payload_capacity_kg'] is not None else "Mission-specific / Unknown"
        range_str = f"{v['operating_range_km']} km" if v['operating_range_km'] is not None else "Unknown"
        endurance_str = f"{v['endurance_hours']} hours" if v['endurance_hours'] is not None else "Unknown"
        
        print(f"\nID           : {v['vehicle_id']}")
        print(f"NAME         : {v['vehicle_name']}")
        print(f"MANUFACTURER : {v['manufacturer']}")
        print(f"MOBILITY     : {v['mobility_type']}")
        print(f"ROLES        : {', '.join(v['mission_roles'])}")
        print(f"TERRAIN      : {', '.join(v['terrain_capabilities'])}")
        print(f"PAYLOAD      : {payload_str}")
        print(f"MAX SPEED    : {v['max_speed_kmh']} km/h")
        print(f"RANGE        : {range_str}")
        print(f"ENDURANCE    : {endurance_str}")
        print(f"STATUS       : {v['status']}")
        print(f"SOURCE       : {v['source']}")
        print("-" * 50)
