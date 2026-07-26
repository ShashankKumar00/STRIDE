# Database Design

## Purpose

The database stores all the information required by STRIDE to compare mission requirements with vehicle capabilities and generate recommendations.

---

## 1. Vehicle Database

Stores the engineering specifications of autonomous ground vehicles used for mission evaluation and recommendation.

| Field | Description |
|--------|-------------|
| Vehicle ID | Unique identification number for each vehicle. |
| Vehicle Name | Name or model of the autonomous ground vehicle. |
| Payload Capacity | Maximum load the vehicle can safely carry during a mission. |
| Battery Capacity | Available energy for completing the assigned mission. |
| Ground Clearance | Height between the vehicle's underside and the ground, indicating its ability to navigate uneven terrain. |
| Maximum Speed | Highest operating speed of the vehicle under normal conditions. |
| Turning Radius | Minimum space required by the vehicle to make a complete turn, affecting maneuverability. |
| Terrain Compatibility | Types of terrain (rocky, sandy, muddy, etc.) on which the vehicle can operate effectively. |

---

## 2. Terrain Database

Stores information about different terrain types.

| Field | Description |
|--------|-------------|
| Terrain ID | Unique identifier |
| Terrain Type | Rocky, Sand, Mud, etc. |
| Roughness | Terrain roughness level |
| Slope | Inclination |
| Risk Level | Difficulty level |

---

## 3. Mission Database

Stores mission requirements provided by the user.

| Field | Description |
|--------|-------------|
| Mission ID | Unique identifier |
| Mission Type | Surveillance, Supply, Rescue, etc. |
| Payload Required | Payload needed |
| Terrain Type | Expected terrain |
| Distance | Mission distance |
| Priority | Low, Medium, High |
