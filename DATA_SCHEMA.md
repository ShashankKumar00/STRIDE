# STRIDE — Data Schema Specification (Phase 4)

**Document Status:** Complete Phase 4 Specification  
**Date:** October 2026  
**Author:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Establish a standardized, type-safe data schema for Indian Unmanned Ground Vehicles (UGVs), define data provenance policies, formalize taxonomies for mission roles and operational terrains, and specify the treatment of missing values without synthetic zeros.

---

## 1. Executive Summary

In Phase 0, the project audit identified critical schema and data quality flaws:
- Field key discrepancies (`"role"` in database vs. `"mission_roles"` in scoring engine).
- String values (`"Mission-specific"`, `"N/A"`) stored in numerical fields, triggering silent exceptions and unintended zero-scores.
- Absence of unique primary keys (`vehicle_id`).
- Unaligned categorical taxonomies between GUI comboboxes and database records.
- Complete absence of data verification levels and provenance metadata.

Phase 4 defines the canonical **STRIDE Vehicle Data Schema**. It guarantees:
1. **Zero Data Distortion:** Missing specifications are stored as explicit `None` / `null`, never as synthetic `0` or `100`.
2. **Provenance Tracking:** Every parameter is classified by its source verification status.
3. **Rigorous Taxonomy:** Mission roles and terrain capabilities adhere to fixed, shared enumerations.
4. **Unit Consistency:** SI / metric standards throughout (kg, km, km/h, hours).

---

## 2. Canonical Vehicle Schema Definition

Each vehicle record in the STRIDE database is represented as a structured dictionary adhering to the following schema:

```json
{
  "vehicle_id": "STRING (PK, e.g. 'UGV-IND-001')",
  "vehicle_name": "STRING (e.g. 'MUNTRA-S')",
  "manufacturer": "STRING (e.g. 'DRDO - CVRDE')",
  "mobility_type": "STRING ('Tracked' | 'Wheeled 4x4' | 'Wheeled 6x6' | 'Legged')",
  "mission_roles": [
    "ARRAY OF STRINGS (Standardized Role Taxonomy)"
  ],
  "terrain_capabilities": [
    "ARRAY OF STRINGS (Standardized Terrain Taxonomy)"
  ],
  "payload_capacity_kg": "FLOAT or null (Maximum safe mission payload in kg)",
  "max_speed_kmh": "FLOAT (Maximum operating forward speed in km/h)",
  "operating_range_km": "FLOAT or null (Maximum operational travel radius in km)",
  "endurance_hours": "FLOAT or null (Continuous operation duration in hours)",
  "status": "STRING ('In Service' | 'Developed' | 'Technology Demonstrator' | 'Trials')",
  "source": "STRING (Primary reference citation)",
  "provenance": {
    "payload_capacity": "STRING ('Verified' | 'Source-reported' | 'Derived' | 'Unknown')",
    "max_speed": "STRING ('Verified' | 'Source-reported' | 'Derived' | 'Unknown')",
    "operating_range": "STRING ('Verified' | 'Source-reported' | 'Derived' | 'Unknown')",
    "endurance": "STRING ('Verified' | 'Source-reported' | 'Derived' | 'Unknown')"
  }
}
```

---

## 3. Data Quality & Missing Data Policy

In strict adherence to Sections 19, 20, and 21 of the Master Specification:

### 3.1 Provenance Classification Levels:
1. **Verified:** Officially documented in military acceptance documents, OEM technical manuals, or peer-reviewed defense journals.
2. **Source-reported:** Reported in authoritative defense publications (e.g., DRDO Technology Focus, Janes Defence, Bharat Forge press briefs).
3. **Derived:** Mathematically calculated from related physical parameters (with documented derivation formula).
4. **Unknown:** Parameter not publicly disclosed or mission-dependent.

### 3.2 Missing Data Treatment Rules:
1. **No Synthetic Zeros:** An undisclosed endurance or mission-specific payload must **NEVER** be recorded as `0`. In physics, a payload of 0 kg means the vehicle cannot carry even a pebble; an unknown payload means the capacity is unmeasured or configuration-dependent.
2. **Gatekeeper Handling of Missing Data:**
   - If a mission specifies a hard numeric threshold (e.g., Payload $\ge 100$ kg), a vehicle with `payload_capacity_kg: null` is flagged with a **Data Incompleteness Warning** (`"PAYLOAD_CAPACITY_UNKNOWN"`).
   - In conservative military deployment mode, unknown values cannot guarantee mission safety and are treated as non-compliant for hard thresholds unless explicitly overridden by the planner.
3. **MCDM Preference Handling of Missing Data:**
   - When a feasible vehicle possesses an unknown soft criterion during Stage 2 ranking, the criterion is excluded from that vehicle's vector distance calculation, and the remaining criteria weights are re-normalized locally to maintain unbiased fairness.

---

## 4. Standardized Taxonomies

### 4.1 Mission Role Taxonomy
Both GUI selections and database entries must strictly use these canonical tokens:
- `Reconnaissance` (Light scout, sensor deployment, perimeter surveillance)
- `Surveillance` (Persistent stationary/mobile observation, electro-optical monitoring)
- `Combat / Tactical Support` (Weapon mount, remote weapon station, suppressive fire)
- `EOD / IED Disposal` (Bomb disposal, manipulator arm, explosive disruption)
- `Mine Detection / Clearance` (Ground-penetrating radar, surface mine neutralizer)
- `CBRN Reconnaissance` (Chemical, biological, radiological, nuclear sensor suite)
- `Logistics / Transport / Casualty Evacuation` (High-payload carrier, resupply, stretcher mount)

### 4.2 Operating Terrain Taxonomy
Operational terrains are standardized to map directly to physical traction and obstacle profiles:
- `Paved Road / Urban` (Hard paved surface, city streets, smooth asphalt)
- `Plain / Grassland` (Off-road firm dirt, dry soil, rolling grass)
- `Desert / Sand` (Loose sand, sand dunes, desert flats)
- `Mud / Soft Ground` (Waterlogged soil, deep mud, marsh edges)
- `Rugged / Mountainous / Rocky` (Boulders, talus, steep gravel, broken ground)
- `Snow / Ice` (Sub-zero packed/loose snow, ice crust)
- `Extreme Obstacles / Stairs / Confined Spaces` (Urban staircases, interior rubbled corridors)

---

## 5. Standardized 10-UGV Master Dataset

Below is the normalized master dataset for STRIDE's 10 Indian UGVs conforming to the Phase 4 schema:

```json
[
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
    "payload_capacity_kg": null,
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
    "payload_capacity_kg": null,
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
    "payload_capacity_kg": null,
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
    "operating_range_km": null,
    "endurance_hours": null,
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
    "endurance_hours": null,
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
    "operating_range_km": null,
    "endurance_hours": null,
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
    "endurance_hours": null,
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
    "payload_capacity_kg": null,
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
```
