# STRIDE System Architecture

## Purpose

The architecture of STRIDE is designed in a modular manner so that each component performs a specific task and can be independently improved or expanded in future versions.

---

## Overall Workflow

```text
User
  │
  ▼
Mission Input
  │
  ▼
Recommendation Engine
  │
  ├──────────────┐
  ▼              ▼
Vehicle DB   Terrain DB
  │              │
  └──────┬───────┘
         ▼
Decision Logic
         │
         ▼
Vehicle Recommendation
         │
         ▼
Mission Simulation
         │
         ▼
Mission Report
```

---

## Modules

### 1. Mission Module

Collects mission details such as:
- Mission type
- Payload
- Terrain
- Distance
- Priority

---

### 2. Vehicle Database

Stores the specifications of all available autonomous ground vehicles.

---

### 3. Terrain Database

Stores terrain properties required for comparison.

---

### 4. Recommendation Engine

Compares mission requirements with vehicle specifications and identifies the most suitable vehicle.

---

### 5. Simulation Module

Provides a basic visualization of the selected vehicle performing the mission.

---

### 6. Report Generator

Generates a summary containing:
- Mission details
- Selected vehicle
- Reason for recommendation
- Simulation outcome
