# Database Design

## Purpose

The database stores all the information required by STRIDE to compare mission requirements with vehicle capabilities and generate recommendations.

---

## 1. Vehicle Database

Stores the specifications of each autonomous ground vehicle.

| Field | Description |
|--------|-------------|
| Vehicle ID | Unique identifier |
| Vehicle Name | Name of the vehicle |
| Payload Capacity | Maximum payload |
| Battery Capacity | Available battery |
| Ground Clearance | Distance from ground |
| Maximum Speed | Top speed |
| Turning Radius | Turning capability |
| Terrain Compatibility | Supported terrains |

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
