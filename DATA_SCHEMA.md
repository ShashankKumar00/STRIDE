# STRIDE — Data Schema Specification (Phase 4 & Extended Catalog)

**Document Status:** Complete Phase 4 & Extended Catalog Specification  
**Date:** October 2026  
**Author:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Establish a standardized, type-safe data schema for Indian Unmanned Ground Vehicles (UGVs), define data provenance policies, formalize taxonomies for mission roles and operational terrains, specify tactical communication links, climate/altitude envelopes, stealth acoustic/thermal signatures, and link each platform to authentic visual assets without synthetic zeros.

---

## 1. Executive Summary

In Phase 0, the project audit identified critical schema and data quality flaws:
- Field key discrepancies (`"role"` in database vs. `"mission_roles"` in scoring engine).
- String values (`"Mission-specific"`, `"N/A"`) stored in numerical fields, triggering silent exceptions and unintended zero-scores.
- Absence of unique primary keys (`vehicle_id`).
- Unaligned categorical taxonomies between GUI comboboxes and database records.
- Complete absence of data verification levels and provenance metadata.

The extended schema guarantees:
1. **Zero Data Distortion:** Missing specifications are stored as explicit `None` / `null`, never as synthetic `0` or `100`.
2. **Provenance Tracking:** Every parameter is classified by its source verification status.
3. **Rigorous Taxonomy:** Mission roles, terrain capabilities, control links, and stealth profiles adhere to fixed, shared enumerations.
4. **Unit Consistency:** SI / metric standards throughout (kg, km, km/h, hours, meters ASL, Celsius, decibels).
5. **Authentic Visual Imagery:** Every vehicle is paired with verified photographic or high-resolution visual reference assets stored in `assets/images/`.

---

## 2. Canonical Vehicle Schema Definition

Each vehicle record in the STRIDE database is represented as a structured dictionary adhering to the following schema:

```json
{
  "vehicle_id": "STRING (PK, e.g. 'UGV-IND-001')",
  "vehicle_name": "STRING (e.g. 'MUNTRA-S')",
  "manufacturer": "STRING (e.g. 'DRDO - CVRDE')",
  "mobility_type": "STRING ('Tracked' | 'Wheeled 4x4' | 'Wheeled 6x6' | 'Wheeled 8x8' | 'Quadruped (Robot Dog)')",
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
  "max_control_range_km": "FLOAT or null (Maximum operator standoff distance in km)",
  "control_link_types": [
    "ARRAY OF STRINGS ('RF LOS' | 'COFDM NLOS' | 'Fiber-Optic' | 'SATCOM / Drone Relay' | 'Autonomous SLAM')"
  ],
  "climate_altitude": {
    "min_operating_temp_c": "FLOAT (Minimum operating temperature in deg C)",
    "max_operating_temp_c": "FLOAT (Maximum operating temperature in deg C)",
    "max_altitude_m_asl": "INTEGER (Maximum operational altitude in meters Above Sea Level)",
    "cold_start_capable": "BOOLEAN"
  },
  "stealth_profile": {
    "propulsion_type": "STRING ('All-Electric (Silent)' | 'Hybrid-Electric' | 'Diesel / IC Engine')",
    "acoustic_stealth_db_at_10m": "FLOAT (Sound pressure level in dBA at 10m distance)",
    "thermal_signature_level": "STRING ('Very Low' | 'Low' | 'Medium' | 'High')"
  },
  "status": "STRING ('In Service' | 'Under Procurement / Induction' | 'In Production' | 'Field Trials / Evaluated' | 'Developed / Demonstrated' | 'Technology Demonstrator')",
  "source": "STRING (Primary reference citation)",
  "image_path": "STRING (Path to vehicle image asset, e.g. 'assets/images/muntra_s.jpg')",
  "provenance": {
    "payload_capacity": "STRING ('Source-reported' | 'Estimated' | 'Unknown')",
    "max_speed": "STRING ('Source-reported' | 'Derived')",
    "operating_range": "STRING ('Source-reported' | 'Estimated' | 'Unknown')",
    "endurance": "STRING ('Source-reported' | 'Estimated' | 'Unknown')",
    "control_range": "STRING ('Source-reported' | 'Estimated')",
    "climate_altitude": "STRING ('Source-reported' | 'Specified')",
    "stealth": "STRING ('Powertrain-derived' | 'Acoustic-tested')"
  }
}
```

---

## 3. Standardized Taxonomies

### 3.1 Mission Roles
- `Surveillance`: Optical, thermal, and electronic observation of areas of interest.
- `Reconnaissance`: Active scouting, forward presence, and path discovery in contested territory.
- `Mine Detection / Clearance`: Identification, scanning, and physical neutralization of surface and buried mines.
- `CBRN Reconnaissance`: Nuclear, biological, chemical detection, air sniffing, and hazardous soil sampling.
- `Combat / Tactical Support`: Weaponized fire support (RCWS, machine guns, anti-tank missiles, direct fire).
- `Logistics / Transport / Casualty Evacuation`: Heavy payload carriage, ammunition delivery, and CASEVAC stretcher transport.
- `EOD / IED Disposal`: Robotic manipulator arm interrogation and water-jet disruption of explosive ordnance.
- `High-Altitude Logistics / Extreme Cold`: Heavy load transport at extreme sub-zero temperatures and altitudes > 4,000m ASL.
- `Precision Strike / Anti-Armor`: Direct kinetic or shaped-charge assault against armored vehicles and fortified bunkers.
- `Urban Assault / Confined Space Recon`: Navigation through building interiors, narrow aircraft/train aisles, and stairways.

### 3.2 Terrains
- `Paved Road / Urban`
- `Plain / Grassland`
- `Desert / Sand`
- `Mud / Soft Ground`
- `Rugged / Mountainous / Rocky`
- `Snow / Ice`
- `Extreme Obstacles / Stairs / Confined Spaces`
- `Amphibious / Riverine / Fording`

### 3.3 Control Link Types
- `RF LOS (Radio Frequency Line of Sight)`
- `COFDM NLOS (Non-Line of Sight Mesh)`
- `Fiber-Optic (Jam-Proof / EW-Immune)`
- `SATCOM / BLOS Drone Relay`
- `Autonomous Waypoint / GNSS-Denied SLAM`

---

## 4. Complete 24 Indian Defence UGV Catalog

| ID | Vehicle Name | Manufacturer | Mobility | Primary Role | Payload (kg) | Speed (km/h) | Range (km) | Standoff (km) | Image Asset |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **001** | MUNTRA-S | DRDO CVRDE | Tracked | Surveillance | *Unknown* | 20.0 | 20.0 | 20.0 | `muntra_s.jpg` |
| **002** | MUNTRA-M | DRDO CVRDE | Tracked | Mine Detection / Clearance | *Unknown* | 20.0 | 20.0 | 20.0 | `muntra_m.jpg` |
| **003** | MUNTRA-N | DRDO CVRDE | Tracked | CBRN Reconnaissance | *Unknown* | 20.0 | 20.0 | 20.0 | `muntra_n.jpg` |
| **004** | ECARS 4x4 | Kalyani / Bharat Forge | Wheeled 4x4 | Multi-Role Tactical | 350.0 | 20.0 | 15.0 | 10.0 | `kalyani_ecars_4x4.jpg` |
| **005** | Mooshak | Dronobotics | Tracked | Mini Scout / Combat | 3.0 | 20.0 | 11.0 | 5.0 | `dronobotics_mooshak.jpg` |
| **006** | BRUTE | Gridbots Technologies | Wheeled 6x6 | Combat / Recon | 50.0 | 10.0 | 20.0 | 5.0 | `gridbots_brute.jpg` |
| **007** | HAWK | Gridbots Technologies | Tracked | EOD / Bomb Disposal | 100.0 | 10.0 | 5.0 | 2.0 | `gridbots_hawk.jpg` |
| **008** | ZEUS | Gridbots Technologies | Tracked | Heavy Combat / Logistics | 1500.0 | 15.0 | 20.0 | 10.0 | `gridbots_zeus.jpg` |
| **009** | Vrishabh | Bhairav / Zen Tech | Wheeled 4x4 | High-Speed Scout / Logistics | 150.0 | 50.0 | 100.0 | 20.0 | `bhairav_vrishabh.jpg` |
| **010** | Daksh Scout | DRDO R&DE | Tracked | Micro Stair Climber Recon | 5.0 | 1.2 | 0.2 | 0.2 | `drdo_daksh_scout.jpg` |
| **011** | DRDO Daksh ROV | DRDO R&DE / BEL | Wheeled 6x6 | EOD / Bomb Disposal | 20.0 | 5.0 | 2.0 | 0.5 | `drdo_daksh_rov.jpg` |
| **012** | DRDO Daksh Mini | DRDO R&DE | Tracked | Confined Space EOD | 8.0 | 2.0 | 0.5 | 0.2 | `drdo_daksh_mini.jpg` |
| **013** | ECARS 6x6 | Kalyani / Bharat Forge | Wheeled 6x6 | Amphibious Combat / Mule | 350.0 | 20.0 | 20.0 | 10.0 | `kalyani_ecars_6x6.jpg` |
| **014** | TASL Tracked UGV | Tata Advanced Systems | Tracked | Heavy Combat / Logistics | 1000.0 | 20.0 | 80.0 | 25.0 | `tasl_tracked_ugv.jpg` |
| **015** | Torus MARS UGV | Torus / Army Design Bureau | Wheeled 4x4 | Modular EOD / Recon | 200.0 | 15.0 | 15.0 | 1.0 | `torus_mars_ugv.jpg` |
| **016** | BEML High-Alt UGV | BEML / Torus Robotics | Wheeled 8x8 | High-Altitude Logistics Mule | 750.0 | 12.0 | 15.0 | 10.0 | `beml_high_altitude_ugv.jpg` |
| **017** | SapperScout 2.0 | Indian Army 7 Engr Regt | Wheeled 6x6 | GPR Mine Breacher / CASEVAC | 900.0 | 15.0 | 15.0 | 8.0 | `sapperscout_2_0.jpg` |
| **018** | Xploder UGV | Indian Army 7 Engr Regt | Wheeled 4x4 | Assault / Kamikaze / EOD | 30.0 | 18.0 | 5.0 | 3.0 | `xploder_ugv.jpg` |
| **019** | Gridbots TITAN | Gridbots Technologies | Tracked | Heavy Combat / Minelayer | 1500.0 | 20.0 | 20.0 | 10.0 | `gridbots_titan.jpg` |
| **020** | Gridbots mineHAWK | Gridbots Technologies | Tracked | HAZMAT / Slope Demining | 500.0 | 10.0 | 2.0 | 2.0 | `gridbots_minehawk.jpg` |
| **021** | Zen Prahasta | Zen Technologies | Quadruped | AI Combat Robot Dog | 15.0 | 11.0 | 6.0 | 3.0 | `zen_prahasta.jpg` |
| **022** | Club First Krushna | Club First Robotics | Tracked | Heavy ATGM Combat | 1000.0 | 10.0 | 10.0 | 4.0 | `clubfirst_krushna_ugv.png` |
| **023** | BSS GOLIATH-200 | BSS Alliance | Tracked | Fiber-Optic Strike UGV | 200.0 | 15.0 | 10.0 | 10.0 | `bss_goliath_200.jpg` |
| **024** | Svaayatt SGV-500 | Svaayatt Systems | Tracked | Drone-Relayed Combat | 200.0 | 30.0 | 40.0 | 25.0 | `svaayatt_sgv_500.jpg` |
