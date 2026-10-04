# Standardized Vehicle Database for STRIDE
# Expanded Indian Defence UGV Catalog (24 Platforms)
# Conforms to Phase 4 DATA_SCHEMA.md and Phase 6 Decision Methodology

VEHICLE_DATABASE = [
    # ---------------------------------------------------------
    # 1. MUNTRA-S (DRDO CVRDE)
    # ---------------------------------------------------------
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
        "max_control_range_km": 20.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 52.0,
            "max_altitude_m_asl": 4000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Diesel / IC Engine",
            "acoustic_stealth_db_at_10m": 82.0,
            "thermal_signature_level": "Medium"
        },
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus & SPS Land Forces",
        "image_path": "assets/images/muntra_s.jpg",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported",
            "control_range": "Source-reported",
            "climate_altitude": "Source-reported (Mahajan trials up to 52C)",
            "stealth": "Engine-based"
        }
    },

    # ---------------------------------------------------------
    # 2. MUNTRA-M (DRDO CVRDE)
    # ---------------------------------------------------------
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
        "max_control_range_km": 20.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 52.0,
            "max_altitude_m_asl": 4000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Diesel / IC Engine",
            "acoustic_stealth_db_at_10m": 82.0,
            "thermal_signature_level": "Medium"
        },
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus & CVRDE Reports",
        "image_path": "assets/images/muntra_m.jpg",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported",
            "control_range": "Source-reported",
            "climate_altitude": "Source-reported",
            "stealth": "Engine-based"
        }
    },

    # ---------------------------------------------------------
    # 3. MUNTRA-N (DRDO CVRDE)
    # ---------------------------------------------------------
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
        "max_control_range_km": 20.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 52.0,
            "max_altitude_m_asl": 4000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Diesel / IC Engine",
            "acoustic_stealth_db_at_10m": 82.0,
            "thermal_signature_level": "Medium"
        },
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus & CVRDE Reports",
        "image_path": "assets/images/muntra_n.jpg",
        "provenance": {
            "payload_capacity": "Unknown",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported",
            "control_range": "Source-reported",
            "climate_altitude": "Source-reported",
            "stealth": "Engine-based"
        }
    },

    # ---------------------------------------------------------
    # 4. ECARS 4x4 (Kalyani / Bharat Forge)
    # ---------------------------------------------------------
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
        "operating_range_km": 15.0,
        "endurance_hours": 6.0,
        "max_control_range_km": 10.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 48.0,
            "thermal_signature_level": "Low"
        },
        "status": "Developed / Demonstrated",
        "source": "Bharat Forge - ECARS Brief & DefExpo Showcase",
        "image_path": "assets/images/kalyani_ecars_4x4.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (350 kg)",
            "max_speed": "Source-reported (16-20 km/h)",
            "operating_range": "Manufacturer estimated",
            "endurance": "Estimated from battery pack",
            "control_range": "Source-reported",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Electric powertrain"
        }
    },

    # ---------------------------------------------------------
    # 5. Mooshak (Dronobotics)
    # ---------------------------------------------------------
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
        "max_control_range_km": 5.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -10.0,
            "max_operating_temp_c": 45.0,
            "max_altitude_m_asl": 4200,
            "cold_start_capable": False
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 42.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "Developed",
        "source": "Dronobotics - Mooshak UGV Specification",
        "image_path": "assets/images/dronobotics_mooshak.jpg",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported",
            "control_range": "Source-reported",
            "climate_altitude": "Trial reported",
            "stealth": "Mini electric"
        }
    },

    # ---------------------------------------------------------
    # 6. BRUTE (Gridbots Technologies)
    # ---------------------------------------------------------
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
        "endurance_hours": 8.0,
        "max_control_range_km": 5.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 46.0,
            "thermal_signature_level": "Low"
        },
        "status": "Developed",
        "source": "Gridbots - BRUTE Combat UGV Datasheet",
        "image_path": "assets/images/gridbots_brute.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (50-250 kg modular)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Estimated from battery pack",
            "control_range": "Manufacturer reported",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Electric 6x6"
        }
    },

    # ---------------------------------------------------------
    # 7. HAWK (Gridbots Technologies)
    # ---------------------------------------------------------
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
        "operating_range_km": 5.0,
        "endurance_hours": 6.0,
        "max_control_range_km": 2.0,
        "control_link_types": [
            "RF LOS (Radio Frequency Line of Sight)",
            "COFDM NLOS (Non-Line of Sight Mesh)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -15.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 40.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "Developed",
        "source": "Gridbots - HAWK EOD Robot Datasheet",
        "image_path": "assets/images/gridbots_hawk.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (30 kg arm / 100 kg chassis)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Manufacturer estimated",
            "control_range": "Source-reported (2 km)",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Silent electric EOD"
        }
    },

    # ---------------------------------------------------------
    # 8. ZEUS (Gridbots Technologies)
    # ---------------------------------------------------------
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
        "max_control_range_km": 10.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -25.0,
            "max_operating_temp_c": 52.0,
            "max_altitude_m_asl": 4500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Hybrid-Electric",
            "acoustic_stealth_db_at_10m": 64.0,
            "thermal_signature_level": "Low"
        },
        "status": "Developed",
        "source": "Gridbots - ZEUS Heavy Combat UGV Datasheet",
        "image_path": "assets/images/gridbots_zeus.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (1500 kg)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported (12 hours)",
            "control_range": "Manufacturer reported",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Hybrid powertrain"
        }
    },

    # ---------------------------------------------------------
    # 9. Vrishabh (Bhairav Robotics / Zen Technologies)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-009",
        "vehicle_name": "Vrishabh",
        "manufacturer": "Bhairav Robotics / Zen Technologies",
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
        "endurance_hours": 8.0,
        "max_control_range_km": 20.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "SATCOM / BLOS Drone Relay"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -10.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Hybrid-Electric",
            "acoustic_stealth_db_at_10m": 62.0,
            "thermal_signature_level": "Medium"
        },
        "status": "Under Development / Trials",
        "source": "Janes Defence - Bhairav Robotics Vrishabh & Zen Technologies",
        "image_path": "assets/images/bhairav_vrishabh.jpg",
        "provenance": {
            "payload_capacity": "Source-reported",
            "max_speed": "Source-reported (50 km/h high-speed)",
            "operating_range": "Source-reported (100 km)",
            "endurance": "Estimated from fuel/battery system",
            "control_range": "Source-reported",
            "climate_altitude": "Field trial specified",
            "stealth": "Hybrid low-profile"
        }
    },

    # ---------------------------------------------------------
    # 10. Daksh Scout (DRDO R&DE Engineers)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-010",
        "vehicle_name": "Daksh Scout",
        "manufacturer": "DRDO - R&DE (Engineers)",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Reconnaissance",
            "Surveillance",
            "Urban Assault / Confined Space Recon"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 5.0,
        "max_speed_kmh": 1.2,
        "operating_range_km": 0.2,
        "endurance_hours": 2.0,
        "max_control_range_km": 0.2,
        "control_link_types": [
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -10.0,
            "max_operating_temp_c": 45.0,
            "max_altitude_m_asl": 3000,
            "cold_start_capable": False
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 36.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "Developed / In Service",
        "source": "DRDO - Daksh Scout Technical Specification",
        "image_path": "assets/images/drdo_daksh_scout.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (sensor head)",
            "max_speed": "Source-reported (1.2 km/h stair climbing)",
            "operating_range": "Source-reported (200m)",
            "endurance": "Source-reported (2.0 h)",
            "control_range": "Source-reported (200m LOS)",
            "climate_altitude": "Urban/building rated",
            "stealth": "Micro silent crawler"
        }
    },

    # ---------------------------------------------------------
    # 11. DRDO Daksh ROV (DRDO R&DE / BEL)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-011",
        "vehicle_name": "DRDO Daksh ROV",
        "manufacturer": "DRDO - R&DE (Engineers) / BEL",
        "mobility_type": "Wheeled 6x6",
        "mission_roles": [
            "EOD / IED Disposal",
            "Reconnaissance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 20.0,
        "max_speed_kmh": 5.0,
        "operating_range_km": 2.0,
        "endurance_hours": 3.0,
        "max_control_range_km": 0.5,
        "control_link_types": [
            "RF LOS (Radio Frequency Line of Sight)",
            "Fiber-Optic (Jam-Proof / EW-Immune)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 38.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "In Service",
        "source": "DRDO R&DE Pune / Army Technology Daksh Datasheet",
        "image_path": "assets/images/drdo_daksh_rov.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (20 kg arm lift at 2.5m)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported (3.0 hours battery)",
            "control_range": "Source-reported (500m LOS/cabled)",
            "climate_altitude": "Defence specification standard",
            "stealth": "Battery electric"
        }
    },

    # ---------------------------------------------------------
    # 12. DRDO Daksh Mini / CSROV (DRDO R&DE)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-012",
        "vehicle_name": "DRDO Daksh Mini",
        "manufacturer": "DRDO - R&DE (Engineers)",
        "mobility_type": "Tracked",
        "mission_roles": [
            "EOD / IED Disposal",
            "Urban Assault / Confined Space Recon"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 8.0,
        "max_speed_kmh": 2.0,
        "operating_range_km": 0.5,
        "endurance_hours": 2.5,
        "max_control_range_km": 0.2,
        "control_link_types": [
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -10.0,
            "max_operating_temp_c": 45.0,
            "max_altitude_m_asl": 3000,
            "cold_start_capable": False
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 35.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "In Service",
        "source": "DRDO Confined Space ROV (CSROV) Official Specification",
        "image_path": "assets/images/drdo_daksh_mini.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (8 kg arm lift)",
            "max_speed": "Source-reported (2 km/h)",
            "operating_range": "Source-reported",
            "endurance": "Source-reported (2.5 hours)",
            "control_range": "Source-reported (200m backpack Master Control Station)",
            "climate_altitude": "Aircraft/train rated",
            "stealth": "Ultra-quiet electric"
        }
    },

    # ---------------------------------------------------------
    # 13. ECARS 6x6 (Kalyani Strategic Systems / Bharat Forge)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-013",
        "vehicle_name": "ECARS 6x6",
        "manufacturer": "Kalyani Strategic Systems / Bharat Forge",
        "mobility_type": "Wheeled 6x6",
        "mission_roles": [
            "Surveillance",
            "Combat / Tactical Support",
            "Logistics / Transport / Casualty Evacuation"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Amphibious / Riverine / Fording"
        ],
        "payload_capacity_kg": 350.0,
        "max_speed_kmh": 20.0,
        "operating_range_km": 20.0,
        "endurance_hours": 8.0,
        "max_control_range_km": 10.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -40.0,
            "max_operating_temp_c": 40.0,
            "max_altitude_m_asl": 4500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 46.0,
            "thermal_signature_level": "Low"
        },
        "status": "Developed / Demonstrated",
        "source": "Bharat Forge - ECARS 6x6 Amphibious Specification & DefExpo",
        "image_path": "assets/images/kalyani_ecars_6x6.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (350 kg payload / 500 kg towing)",
            "max_speed": "Source-reported (20 km/h)",
            "operating_range": "Manufacturer reported",
            "endurance": "Estimated from battery pack",
            "control_range": "Manufacturer specified",
            "climate_altitude": "Source-reported (-40C to +40C cold weather rated)",
            "stealth": "Amphibious electric"
        }
    },

    # ---------------------------------------------------------
    # 14. TASL Tracked UGV (Tata Advanced Systems Limited)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-014",
        "vehicle_name": "TASL Tracked UGV",
        "manufacturer": "Tata Advanced Systems Limited",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Combat / Tactical Support",
            "Logistics / Transport / Casualty Evacuation",
            "Surveillance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": 1000.0,
        "max_speed_kmh": 20.0,
        "operating_range_km": 80.0,
        "endurance_hours": 12.0,
        "max_control_range_km": 25.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "SATCOM / BLOS Drone Relay",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -30.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 5000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Hybrid-Electric",
            "acoustic_stealth_db_at_10m": 58.0,
            "thermal_signature_level": "Low"
        },
        "status": "Field Trials / Evaluated",
        "source": "Tata Advanced Systems / Indian Military Review Datasheet",
        "image_path": "assets/images/tasl_tracked_ugv.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (1,000 kg)",
            "max_speed": "Source-reported (20 km/h)",
            "operating_range": "Source-reported (80 km hybrid range)",
            "endurance": "Estimated from hybrid generator",
            "control_range": "Manufacturer reported",
            "climate_altitude": "Himalayan trial rated",
            "stealth": "Dual hybrid powertrain"
        }
    },

    # ---------------------------------------------------------
    # 15. Torus MARS UGV (Torus Robotics / Army Design Bureau)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-015",
        "vehicle_name": "Torus MARS UGV",
        "manufacturer": "Torus Robotics / Army Design Bureau",
        "mobility_type": "Wheeled 4x4",
        "mission_roles": [
            "EOD / IED Disposal",
            "Reconnaissance",
            "Surveillance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": 200.0,
        "max_speed_kmh": 15.0,
        "operating_range_km": 15.0,
        "endurance_hours": 6.0,
        "max_control_range_km": 1.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -35.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 5200,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 38.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "In Service / Inducted",
        "source": "Torus Robotics MARS V2 / Army Design Bureau / iDEX",
        "image_path": "assets/images/torus_mars_ugv.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (modular 200 kg)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported",
            "endurance": "Source-reported (6 hours)",
            "control_range": "Source-reported (1.0 km remote IED standoff)",
            "climate_altitude": "Source-reported (Siachen / Ladakh high-altitude tested)",
            "stealth": "Indigenous axial-flux silent electric"
        }
    },

    # ---------------------------------------------------------
    # 16. BEML High-Altitude UGV (BEML / Torus Robotics)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-016",
        "vehicle_name": "BEML High-Altitude UGV",
        "manufacturer": "BEML Limited / Torus Robotics",
        "mobility_type": "Wheeled 8x8",
        "mission_roles": [
            "High-Altitude Logistics / Extreme Cold",
            "Logistics / Transport / Casualty Evacuation"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": 750.0,
        "max_speed_kmh": 12.0,
        "operating_range_km": 15.0,
        "endurance_hours": 8.0,
        "max_control_range_km": 10.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "SATCOM / BLOS Drone Relay",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -40.0,
            "max_operating_temp_c": 40.0,
            "max_altitude_m_asl": 5500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 44.0,
            "thermal_signature_level": "Low"
        },
        "status": "Field Trials / Evaluated",
        "source": "BEML Ltd & Torus MoU Aero India / Northern Command High Altitude Trials",
        "image_path": "assets/images/beml_high_altitude_ugv.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (750 kg high-altitude mule)",
            "max_speed": "Source-reported",
            "operating_range": "Manufacturer reported",
            "endurance": "Source-reported (8.0 hours)",
            "control_range": "Manufacturer specified",
            "climate_altitude": "Source-reported (designed for Ladakh and Siachen at 5500m ASL)",
            "stealth": "Multi-wheel electric drive"
        }
    },

    # ---------------------------------------------------------
    # 17. SapperScout 2.0 (Indian Army / CME Pune)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-017",
        "vehicle_name": "SapperScout 2.0",
        "manufacturer": "Indian Army (7 Engr Regt / CME Pune - Maj Rajprasad RS)",
        "mobility_type": "Wheeled 6x6",
        "mission_roles": [
            "Mine Detection / Clearance",
            "Logistics / Transport / Casualty Evacuation",
            "Surveillance",
            "Combat / Tactical Support"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Snow / Ice"
        ],
        "payload_capacity_kg": 900.0,
        "max_speed_kmh": 15.0,
        "operating_range_km": 15.0,
        "endurance_hours": 6.0,
        "max_control_range_km": 8.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -30.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4800,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 48.0,
            "thermal_signature_level": "Low"
        },
        "status": "Under Procurement / Induction",
        "source": "Indian Army Inno-Yoddha 2025 / Army Design Bureau / CME Pune",
        "image_path": "assets/images/sapperscout_2_0.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (900 kg heavy logistics/mine clearance)",
            "max_speed": "Source-reported",
            "operating_range": "Field reported",
            "endurance": "Field reported",
            "control_range": "Army field trials reported",
            "climate_altitude": "High altitude and plains validated",
            "stealth": "Independent 6-wheel electric drive"
        }
    },

    # ---------------------------------------------------------
    # 18. Xploder UGV (Indian Army / CME Pune)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-018",
        "vehicle_name": "Xploder UGV",
        "manufacturer": "Indian Army (7 Engr Regt / CME Pune - Maj Rajprasad RS)",
        "mobility_type": "Wheeled 4x4",
        "mission_roles": [
            "Combat / Tactical Support",
            "EOD / IED Disposal",
            "Urban Assault / Confined Space Recon",
            "Precision Strike / Anti-Armor"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 30.0,
        "max_speed_kmh": 18.0,
        "operating_range_km": 5.0,
        "endurance_hours": 3.5,
        "max_control_range_km": 3.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "RF LOS (Radio Frequency Line of Sight)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4200,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 42.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "In Service / Inducted",
        "source": "Indian Army COAS Induction Dec 2024 / Aero India 2025 India Pavilion",
        "image_path": "assets/images/xploder_ugv.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (30 kg explosive charge / sensor arm)",
            "max_speed": "Source-reported (18 km/h)",
            "operating_range": "Source-reported (5 km)",
            "endurance": "Source-reported (3.5 hours)",
            "control_range": "Army trials reported",
            "climate_altitude": "Counter-insurgency operational rating",
            "stealth": "Low-profile electric assault"
        }
    },

    # ---------------------------------------------------------
    # 19. Gridbots TITAN (Gridbots Technologies)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-019",
        "vehicle_name": "Gridbots TITAN",
        "manufacturer": "Gridbots Technologies",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Combat / Tactical Support",
            "Mine Detection / Clearance",
            "Logistics / Transport / Casualty Evacuation"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 1500.0,
        "max_speed_kmh": 20.0,
        "operating_range_km": 20.0,
        "endurance_hours": 12.0,
        "max_control_range_km": 10.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "Hybrid-Electric",
            "acoustic_stealth_db_at_10m": 62.0,
            "thermal_signature_level": "Low"
        },
        "status": "In Production",
        "source": "Gridbots Technologies - TITAN Series & Titan Fortifier Datasheet",
        "image_path": "assets/images/gridbots_titan.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (1500 kg / 50 anti-tank mines)",
            "max_speed": "Source-reported (20 km/h)",
            "operating_range": "Source-reported",
            "endurance": "Source-reported (12 hours)",
            "control_range": "Manufacturer reported",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Hybrid tracked heavy platform"
        }
    },

    # ---------------------------------------------------------
    # 20. Gridbots mineHAWK (Gridbots Technologies)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-020",
        "vehicle_name": "Gridbots mineHAWK",
        "manufacturer": "Gridbots Technologies",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Mine Detection / Clearance",
            "EOD / IED Disposal",
            "CBRN Reconnaissance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 500.0,
        "max_speed_kmh": 10.0,
        "operating_range_km": 2.0,
        "endurance_hours": 8.0,
        "max_control_range_km": 2.0,
        "control_link_types": [
            "RF LOS (Radio Frequency Line of Sight)",
            "COFDM NLOS (Non-Line of Sight Mesh)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -15.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 3800,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 40.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "In Production",
        "source": "Gridbots Technologies - GB-MHAWK HAZMAT / Demining Datasheet",
        "image_path": "assets/images/gridbots_minehawk.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (500 kg)",
            "max_speed": "Source-reported",
            "operating_range": "Source-reported (2 km)",
            "endurance": "Source-reported (8 hours)",
            "control_range": "Source-reported (2 km)",
            "climate_altitude": "Manufacturer specified",
            "stealth": "Hazard-sealed electric"
        }
    },

    # ---------------------------------------------------------
    # 21. Zen Prahasta (Zen Technologies / AI Turing)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-021",
        "vehicle_name": "Zen Prahasta",
        "manufacturer": "Zen Technologies / AI Turing Technologies",
        "mobility_type": "Quadruped (Robot Dog)",
        "mission_roles": [
            "Urban Assault / Confined Space Recon",
            "Combat / Tactical Support",
            "Reconnaissance",
            "Surveillance"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Rugged / Mountainous / Rocky",
            "Extreme Obstacles / Stairs / Confined Spaces"
        ],
        "payload_capacity_kg": 15.0,
        "max_speed_kmh": 11.0,
        "operating_range_km": 6.0,
        "endurance_hours": 3.0,
        "max_control_range_km": 3.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -15.0,
            "max_operating_temp_c": 45.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 34.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "Field Trials / Evaluated",
        "source": "Zen Technologies Official Product Release - Prahasta Autonomous Quadruped",
        "image_path": "assets/images/zen_prahasta.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (weaponized with 9mm/5.56mm/7.62mm RCWS)",
            "max_speed": "Source-reported (~3 m/s)",
            "operating_range": "Estimated from battery capacity",
            "endurance": "Estimated from operation profile (3 hours)",
            "control_range": "Manufacturer reported",
            "climate_altitude": "Urban counter-insurgency rating",
            "stealth": "Whisper-quiet quadruped electric"
        }
    },

    # ---------------------------------------------------------
    # 22. Club First Krushna UGV (Club First Robotics)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-022",
        "vehicle_name": "Club First Krushna UGV",
        "manufacturer": "Club First Robotics",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Combat / Tactical Support",
            "Precision Strike / Anti-Armor",
            "Logistics / Transport / Casualty Evacuation",
            "EOD / IED Disposal"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 1000.0,
        "max_speed_kmh": 10.0,
        "operating_range_km": 10.0,
        "endurance_hours": 3.0,
        "max_control_range_km": 4.0,
        "control_link_types": [
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 55.0,
            "max_altitude_m_asl": 3500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 45.0,
            "thermal_signature_level": "Low"
        },
        "status": "In Service",
        "source": "Club First Robotics / Indian Army Day & Republic Day Showcase",
        "image_path": "assets/images/clubfirst_krushna_ugv.png",
        "provenance": {
            "payload_capacity": "Source-reported (1,000 kg / 10-ton tow)",
            "max_speed": "Source-reported (10 km/h)",
            "operating_range": "Manufacturer reported",
            "endurance": "Source-reported (180 minutes / 3 hours)",
            "control_range": "Manufacturer specified",
            "climate_altitude": "Source-reported (ATEX certified explosion/high heat proof to 55C)",
            "stealth": "Heavy duty electric tracked"
        }
    },

    # ---------------------------------------------------------
    # 23. BSS GOLIATH-200 (Bharat Supply & Support Alliance)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-023",
        "vehicle_name": "BSS GOLIATH-200",
        "manufacturer": "Bharat Supply & Support (BSS) Alliance",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Precision Strike / Anti-Armor",
            "Combat / Tactical Support"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 200.0,
        "max_speed_kmh": 15.0,
        "operating_range_km": 10.0,
        "endurance_hours": 2.0,
        "max_control_range_km": 10.0,
        "control_link_types": [
            "Fiber-Optic (Jam-Proof / EW-Immune)"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4000,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 36.0,
            "thermal_signature_level": "Very Low"
        },
        "status": "Under Procurement / Induction",
        "source": "Bharat Supply & Support Alliance / Defence News India July 2026",
        "image_path": "assets/images/bss_goliath_200.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (200 kg high-explosive shaped charge)",
            "max_speed": "Manufacturer reported",
            "operating_range": "Source-reported (10 km fiber optic tether)",
            "endurance": "Estimated strike sprint endurance",
            "control_range": "Source-reported (10 km jam-proof fiber tether)",
            "climate_altitude": "Frontline border defense rated",
            "stealth": "Zero radio frequency emissions (EW immune)"
        }
    },

    # ---------------------------------------------------------
    # 24. Svaayatt SGV-500 Scorpion (Svaayatt Systems)
    # ---------------------------------------------------------
    {
        "vehicle_id": "UGV-IND-024",
        "vehicle_name": "Svaayatt SGV-500 Scorpion",
        "manufacturer": "Svaayatt Systems",
        "mobility_type": "Tracked",
        "mission_roles": [
            "Combat / Tactical Support",
            "Surveillance",
            "Reconnaissance",
            "Logistics / Transport / Casualty Evacuation"
        ],
        "terrain_capabilities": [
            "Paved Road / Urban",
            "Plain / Grassland",
            "Desert / Sand",
            "Mud / Soft Ground",
            "Rugged / Mountainous / Rocky"
        ],
        "payload_capacity_kg": 200.0,
        "max_speed_kmh": 30.0,
        "operating_range_km": 40.0,
        "endurance_hours": 5.0,
        "max_control_range_km": 25.0,
        "control_link_types": [
            "SATCOM / BLOS Drone Relay",
            "COFDM NLOS (Non-Line of Sight Mesh)",
            "Autonomous Waypoint / GNSS-Denied SLAM"
        ],
        "climate_altitude": {
            "min_operating_temp_c": -20.0,
            "max_operating_temp_c": 50.0,
            "max_altitude_m_asl": 4500,
            "cold_start_capable": True
        },
        "stealth_profile": {
            "propulsion_type": "All-Electric (Silent)",
            "acoustic_stealth_db_at_10m": 44.0,
            "thermal_signature_level": "Low"
        },
        "status": "Field Trials / Evaluated",
        "source": "Svaayatt Systems / Indian Army ACC&S Ahilyanagar Field Trials",
        "image_path": "assets/images/svaayatt_sgv_500.jpg",
        "provenance": {
            "payload_capacity": "Source-reported (200 kg payload / 500 kg gross weight)",
            "max_speed": "Source-reported (30 km/h fast tracked)",
            "operating_range": "Source-reported (40 km on single charge)",
            "endurance": "Source-reported (5.0 hours)",
            "control_range": "Source-reported (25 km via integrated drone relay bridge)",
            "climate_altitude": "Armoured Corps field trials specified",
            "stealth": "Electric tracked with drone relay"
        }
    }
]

# Backward compatibility alias
vehicle_database = VEHICLE_DATABASE


def get_all_vehicles():
    """Returns a copy of the canonical vehicle database."""
    return list(VEHICLE_DATABASE)


def get_vehicle_by_id(vehicle_id: str):
    """Fetches a specific vehicle dictionary by its unique canonical ID."""
    for v in VEHICLE_DATABASE:
        if v.get("vehicle_id") == vehicle_id:
            return dict(v)
    return None


def get_vehicle_by_name(vehicle_name: str):
    """Fetches a specific vehicle dictionary by its platform name."""
    for v in VEHICLE_DATABASE:
        if v.get("vehicle_name", "").lower() == vehicle_name.lower():
            return dict(v)
    return None


def display_all_vehicles():
    """Displays formatted terminal summary of all 24 vehicles."""
    for v in VEHICLE_DATABASE:
        payload_str = f"{v['payload_capacity_kg']} kg" if v['payload_capacity_kg'] is not None else "Mission-specific / Unknown"
        range_str = f"{v['operating_range_km']} km" if v['operating_range_km'] is not None else "Unknown"
        endurance_str = f"{v['endurance_hours']} hours" if v['endurance_hours'] is not None else "Unknown"
        control_str = f"{v['max_control_range_km']} km" if v.get('max_control_range_km') is not None else "Direct line of sight"
        
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
        print(f"CONTROL LINK : {control_str} [{', '.join(v.get('control_link_types', []))}]")
        print(f"IMAGE ASSET  : {v.get('image_path', 'N/A')}")
        print(f"STATUS       : {v['status']}")
        print(f"SOURCE       : {v['source']}")
        print("-" * 60)
