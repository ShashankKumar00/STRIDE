# Vehicle Database for STRIDE

vehicle_database = [
    {
        "vehicle_name": "MUNTRA-S",
        "manufacturer": "DRDO - CVRDE",
        "role": ["Surveillance", "reconnaissance"],
        "terrain": ["All Terrain"],
        "payload_capacity": "Mission-specific",
        "max_speed": 20,
        "endurance": 8,
        "operating_range": 20,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus"
    },
    {
        "vehicle_name": "MUNTRA-M",
        "manufacturer": "DRDO - CVRDE",
        "role": ["Mine detection", "marking"],
        "terrain": ["All Terrain"],
        "payload_capacity": "Mission-specific",
        "max_speed": 20,
        "endurance": 8,
        "operating_range": 20,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus"
    },
    {
        "vehicle_name": "MUNTRA-N",
        "manufacturer": "DRDO - CVRDE",
        "role": ["NBC / CBRN reconnaissance"],
        "terrain": ["All Terrain"],
        "payload_capacity": "Mission-specific",
        "max_speed": 20,
        "endurance": 8,
        "operating_range": 20,
        "status": "Technology Demonstrator",
        "source": "DRDO - MUNTRA UGV Technology Focus"
    },
    {
        "vehicle_name": "ECARS 4x4",
        "manufacturer": "Kalyani Strategic Systems / Bharat Forge",
        "role": ["Surveillance", "security", "safety", "rescue"],
        "terrain": ["Mud", "Sand", "Multi Terrain", "All Weather"],
        "payload_capacity": 350,
        "max_speed": 20,
        "endurance": "N/A",
        "operating_range": "N/A",
        "status": "Developed / Demonstrated",
        "source": "Bharat Forge - ECARS"
    },
    {
        "vehicle_name": "Mooshak",
        "manufacturer": "Dronobotics",
        "role": ["Multi-role military support"],
        "terrain": ["Rough Terrain", "Off Road"],
        "payload_capacity": 3,
        "max_speed": 20,
        "endurance": 8,
        "operating_range": 11,
        "status": "Developed",
        "source": "Dronobotics - Mooshak UGV"
    },
    {
        "vehicle_name": "BRUTE",
        "manufacturer": "Gridbots Technologies",
        "role": ["Combat, surveillance", "tactical support"],
        "terrain": ["All Terrain"],
        "payload_capacity": 50,
        "max_speed": 10,
        "endurance": "N/A",
        "operating_range": 20,
        "status": "Developed",
        "source": "Gridbots - BRUTE Combat UGV"
    },
    {
        "vehicle_name": "HAWK",
        "manufacturer": "Gridbots Technologies",
        "role": ["EOD", "IED disposal", "reconnaissance"],
        "terrain": ["Rough Terrain", "Urban", "Stairs"],
        "payload_capacity": 100,
        "max_speed": 10,
        "endurance": "N/A",
        "operating_range": "N/A",
        "status": "Developed",
        "source": "Gridbots - HAWK EOD Robot"
    },
    {
        "vehicle_name": "ZEUS",
        "manufacturer": "Gridbots Technologies",
        "role": ["Combat", "logistics", "mine clearance", "surveillance"],
        "terrain": ["All Terrain", "Rough Terrain"],
        "payload_capacity": 1500,
        "max_speed": 15,
        "endurance": 12,
        "operating_range": 20,
        "status": "Developed",
        "source": "Gridbots - ZEUS Combat UGV"
    },
    {
        "vehicle_name": "Vrishabh",
        "manufacturer": "Bhairav Robotics",
        "role": ["Combat", "ISR", "casualty evacuation", "logistics"],
        "terrain": ["Desert", "Plains", "Rough Terrain"],
        "payload_capacity": 150,
        "max_speed": 50,
        "endurance": "N/A",
        "operating_range": 100,
        "status": "Under Development / Trials",
        "source": "Janes - Bhairav Robotics Vrishabh"
    },
    {
        "vehicle_name": "Daksh Scout",
        "manufacturer": "DRDO",
        "role": ["Reconnaissance", "surveillance"],
        "terrain": ["Rough Terrain", "Stairs", "Urban"],
        "payload_capacity": "N/A",
        "max_speed": 1.2,
        "endurance": 2,
        "operating_range": 0.2,
        "status": "Developed",
        "source": "DRDO - Daksh Scout"
    }
]


def display_all_vehicles():
    for vehicle in vehicle_database:
        print(f"\nNAME         : {vehicle['vehicle_name']}")
        print(f"MANUFACTURER : {vehicle['manufacturer']}")
        print(f"ROLE         : {vehicle['role']}")
        print(f"TERRAIN      : {', '.join(vehicle['terrain'])}")
        print(f"PAYLOAD      : {vehicle['payload_capacity']}")
        print(f"MAX SPEED    : {vehicle['max_speed']} km/h")
        print(f"ENDURANCE    : {vehicle['endurance']} hours")
        print(f"RANGE        : {vehicle['operating_range']} km")
        print(f"STATUS       : {vehicle['status']}")
        print("-" * 40)


def add_vehicle(new_vehicle):
    vehicle_database.append(new_vehicle)