# STRIDE — Phase 1 Requirement Audit & Parameter Specification

**Document Status:** Complete Phase 1 Specification  
**Date:** October 2026  
**Auditor:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Formalize all user inputs, derived values, stored data, calculated metrics, display elements, mandatory/optional rules, and hard constraints vs. soft preferences in accordance with the Master Specification (Section 30, Phase 1).

---

## 1. Executive Summary

Phase 0 audited the existing code and identified severe logical bottlenecks, including role/terrain string mismatches, conflation of range and distance, lack of hard constraints, and missing-data penalties.

Phase 1 establishes the **formal requirement contract** for STRIDE. It defines exactly:
- What the user inputs,
- What the system derives internally,
- What is stored in the database,
- What calculations are performed,
- What the user sees,
- Which inputs are mandatory vs. optional, and
- The rigorous boundary between **Hard Feasibility Constraints** and **Soft Multi-Criteria Preferences**.

---

## 2. Requirement Classification Matrix

| Parameter | Type / Source | Mandatory? | Hard Constraint? | Soft Preference? | Measurement Unit | Notes / Policy |
|---|---|---|---|---|---|---|
| **Mission Role** | User Input (Dropdown) | **Yes** | **YES (Gatekeeper)** | No | Categorical | If vehicle lacks required capability, vehicle is marked **INFEASIBLE**. |
| **Terrain Type** | User Input (Dropdown) | **Yes** | **YES (Threshold)** | Yes (Traversability) | Categorical | Vehicle must support the operational terrain to enter candidate ranking. |
| **Required Payload** | User Input (Numeric) | **Yes** | **YES (Threshold)** | Yes (Reserve margin) | kg | Vehicle payload capacity must be $\ge$ required payload. |
| **Mission Route Distance** | User Input (Numeric) | **Yes** | **YES (Threshold)** | Yes (Range reserve) | km | Distinct from vehicle operating range. Must be $>0$. |
| **Maximum Mission Time** | User Input (Numeric) | **Yes** | **YES (Deadline)** | Yes (Time margin) | hours | Hard operational ceiling. Defines minimum required speed. |
| **Minimum Mission Time** | User Input (Numeric) | **No** (Optional) | No | Yes (Loiter window) | hours | Used only if mission specifies minimum loitering/patrol duration. |
| **Criterion Priorities** | User Input (Selectors) | **Yes** | No | Weights (1–5 or AHP) | Scale (Very Low–Very High) | Direct user weighting for MCDM ranking. |
| **Vehicle Operating Range** | Stored Vehicle Spec | DB Stored | Evaluated against distance | Preference | km | Tested against Mission Distance $\times$ Safety Margin ($1.25\times$). |
| **Vehicle Max Speed** | Stored Vehicle Spec | DB Stored | Evaluated against required speed | Preference | km/h | Tested against minimum required speed to beat deadline. |
| **Vehicle Endurance** | Stored Vehicle Spec | DB Stored | Evaluated against mission time | Preference | hours | Total continuous operational time available. |
| **Required Speed** | **Derived Internal** | Automatic | Derived Constraint | Preference benchmark | km/h | $\text{Distance} / \text{Max Time}$. Never prompted to user. |
| **Estimated Travel Time**| **Derived Internal** | Automatic | Derived Metric | Preference benchmark | hours | $\text{Distance} / \text{Vehicle Speed}$. |
| **Required Endurance** | **Derived Internal** | Automatic | Derived Constraint | Preference benchmark | hours | $\text{Estimated Time} \times 1.25$. |

---

## 3. Detailed Parameter Breakdown

### 3.1 What Does the User Enter?

The mission planner interacts with a clean, defense-oriented interface to describe the mission scenario:

1. **Mission Role (Mandatory):**
   - Single selection from standardized tactical roles:
     - `Reconnaissance`
     - `Surveillance`
     - `Combat / Tactical Support`
     - `EOD / IED Disposal`
     - `Mine Detection / Clearance`
     - `CBRN Reconnaissance`
     - `Logistics / Transport / Casualty Evacuation`
   - *Rationale:* Defence users plan missions around tactical operational objectives, not vehicle blueprints.

2. **Terrain Type (Mandatory):**
   - Single selection from standardized operating environments:
     - `Paved Road / Urban`
     - `Plain / Grassland`
     - `Desert / Sand`
     - `Mud / Soft Ground`
     - `Rugged / Mountainous / Rocky`
     - `Snow / Ice`
     - `Extreme Obstacles / Stairs / Confined Spaces`

3. **Required Payload (kg) (Mandatory):**
   - Strictly positive numeric input representing the mass of sensors, weapons, supplies, or mission packages to be carried.

4. **Mission Distance (km) (Mandatory):**
   - Strictly positive numeric input representing the expected round-trip or ingress/egress operational distance.
   - *Correction from Prototype:* Replaces the ambiguous "Operating Range" label so users enter mission need, not vehicle specifications.

5. **Maximum Mission Time (hours) (Mandatory):**
   - Strictly positive operational deadline. The vehicle must accomplish the transit and mission within this window.

6. **Minimum Mission Time (hours) (Optional, default = 0):**
   - Optional window. Only utilized if the mission mandates station-keeping, lingering surveillance, or stealth persistence.

7. **Criteria Priorities (Mandatory):**
   - 5-level scale (`Very High`, `High`, `Medium`, `Low`, `Very Low`) for visible trade-off parameters:
     - Payload Importance
     - Range / Distance Margin Importance
     - Speed / Mission Promptness Importance
     - Endurance / Persistence Importance
     - Terrain Compatibility Importance

---

### 3.2 What is Derived Internally?

The system hides technical engineering math behind higher-level mission requirements:

1. **Required Operational Speed ($\text{Speed}_{\text{req}}$):**
   $$\text{Speed}_{\text{req}} = \frac{\text{Mission Distance}}{\text{Maximum Mission Time}}$$
   - Represents the minimum sustained transit speed required to avoid mission failure due to timeout.

2. **Estimated Mission Duration ($\text{Time}_{\text{est}}$):**
   $$\text{Time}_{\text{est}} = \frac{\text{Mission Distance}}{\text{Vehicle Max Speed}}$$
   - Estimated transit time under nominal speed conditions.

3. **Required Endurance with Safety Reserve ($\text{Endurance}_{\text{req}}$):**
   $$\text{Endurance}_{\text{req}} = \text{Time}_{\text{est}} \times 1.25$$
   - A standard defence factor of safety ($25\%$ reserve) ensuring the UGV does not deplete power before mission completion.

4. **Required Range with Tactical Reserve ($\text{Range}_{\text{req}}$):**
   $$\text{Range}_{\text{req}} = \text{Mission Distance} \times 1.25$$
   - Accounts for route detours, obstacle avoidance, and tactical repositioning.

5. **Numerical Criterion Weights ($w_j$):**
   - Normalized weights generated from user priorities such that $\sum w_j = 1.0$.

---

### 3.3 What is Stored in the Database?

Each UGV record stores traceable, provenance-backed engineering specifications:

1. **Identity & Metadata:**
   - `vehicle_id` (Unique string identifier, e.g. `UGV-IND-001`)
   - `vehicle_name` (e.g. `"MUNTRA-S"`)
   - `manufacturer` (e.g. `"DRDO - CVRDE"`)
   - `status` (e.g. `"Technology Demonstrator"`, `"In Service"`, `"Trials"`)
   - `source` (Primary document or literature citation)
   - `provenance` (Data verification level: `Verified`, `Source-reported`, `Derived`, `Unknown`)

2. **Tactical & Environmental Capabilities:**
   - `mission_roles` (List of standardized roles supported)
   - `terrain_capabilities` (List of standardized terrain types traversable)
   - `mobility_type` (`Tracked`, `Wheeled 4x4`, `Wheeled 6x6`, `Legged`)

3. **Performance Limits:**
   - `payload_capacity_kg` (Numerical float or `None` if unknown/mission-specific)
   - `max_speed_kmh` (Numerical float)
   - `operating_range_km` (Numerical float or `None` if unknown)
   - `endurance_hours` (Numerical float or `None` if unknown)

4. **Policy for Non-Numeric / Missing Values:**
   - Values such as `"Mission-specific"` or `"N/A"` are stored as Python `None`.
   - Missing fields are tagged with `provenance: "Unknown"`.
   - **Crucial Rule:** Missing data is never treated as `0` and never treated as `100%`.

---

### 3.4 What is Calculated?

The evaluation follows a **Two-Stage Decision Pipeline**:

```
[Candidate Vehicles]
        │
        ▼
┌──────────────────────────────────────────────┐
│ STAGE 1: Hard Feasibility Filter (Gatekeeper)│
│                                              │
│ 1. Role Check: Mission Role supported?       │
│ 2. Terrain Check: Terrain supported?         │
│ 3. Payload Check: Vehicle Payload >= Req?    │
│ 4. Range Check: Vehicle Range >= Distance?   │
│ 5. Speed Check: Vehicle Speed >= Min Speed?  │
└──────────────────────┬───────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[Infeasible Vehicles]          [Feasible Candidates]
(Excluded from ranking                 │
with explicit failure reasons)         ▼
                       ┌───────────────────────────────┐
                       │ STAGE 2: Multi-Criteria (MCDM)│
                       │          Preference Ranking   │
                       │                               │
                       │ 1. Normalized Benefit Scores  │
                       │ 2. Priority Weighting         │
                       │ 3. Aggregate Suitability Score│
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       [Ranked Vehicles & Top UGV]
```

#### Stage 1: Feasibility Evaluation
For vehicle $i$:
$$\text{Feasible}_i = \text{RoleMatch}_i \land \text{TerrainMatch}_i \land (\text{Payload}_i \ge \text{Payload}_{\text{req}}) \land (\text{Range}_i \ge \text{Distance}) \land (\text{Speed}_i \ge \text{Speed}_{\text{req}})$$
- If any condition is violated, the vehicle is flagged as `Infeasible` with specific failed constraint tokens (e.g., `["PAYLOAD_DEFICIT", "ROLE_UNSUPPORTED"]`).

#### Stage 2: Preference Scoring (for Feasible Vehicles)
Only feasible candidates are ranked across continuous preference criteria:
- **Payload Reserve Score:** How comfortably does the UGV accommodate the payload?
- **Range Safety Margin:** What margin of safety does the UGV provide beyond the route distance?
- **Mission Promptness:** How much faster than the deadline can the UGV complete the mission safely?
- **Endurance Persistence:** How much continuous operating time remains after the transit?
- **Weighted Suitability Score:** Formulated using normalized criteria weights.

---

### 3.5 What is Displayed?

The user-facing presentation will be upgraded from a raw single-number output to a transparent, decision-support briefing:

1. **Executive Recommendation Card:**
   - Name of the Top Recommended UGV.
   - Overall Suitability Score (%).
   - Concise Rationale ("Why Recommended").
   - Summary of Strongest Match Parameters.
   - Identified Operational Constraints or Watch-outs.

2. **Feasible Vehicles Ranking Table:**
   - Rank position (1, 2, 3...)
   - Vehicle Name
   - Overall Suitability Score
   - Parameter breakdown scores (Payload %, Range %, Speed %, Endurance %, Terrain %)

3. **Infeasible Candidates Section (Collapsible / Diagnostic):**
   - Vehicles disqualified by Stage 1 gatekeeper checks.
   - Clear failure explanation (e.g. *"Daksh Scout: Range 0.2 km is insufficient for 10.0 km mission"*).

4. **Audit & Traceability Panel:**
   - Derived values used in the calculation ($\text{Speed}_{\text{req}}$, $\text{Time}_{\text{est}}$, $\text{Endurance}_{\text{req}}$).
   - Provenance tag for any vehicle data with source citations.

---

## 4. Hard Constraints vs. Soft Preferences Summary

| Decision Dimension | Hard Constraint Treatment | Soft Preference Treatment |
|---|---|---|
| **Mission Role** | Binary filter: vehicle must support the role. | None (role is categorical). |
| **Terrain** | Binary filter: vehicle must operate on the terrain. | Degree of ease/traversability (Phase 8+). |
| **Payload** | $\text{Vehicle Payload} < \text{Req Payload} \implies$ **Disqualified**. | $\text{Vehicle Payload} \ge \text{Req Payload} \implies$ Higher reserve scored. |
| **Distance & Range** | $\text{Vehicle Range} < \text{Distance} \implies$ **Disqualified**. | $\text{Vehicle Range} \ge \text{Distance} \implies$ Higher range margin scored. |
| **Time & Speed** | $\text{Vehicle Speed} < \text{Speed}_{\text{req}} \implies$ **Disqualified**. | Higher speed margins score higher promptness. |
| **Endurance** | $\text{Vehicle Endurance} < \text{Time}_{\text{est}} \implies$ **Disqualified**. | Higher endurance beyond transit time scores higher persistence. |

---

## 5. Verification Checklist for Subsequent Phases

- [x] Phase 0 complete: Project baseline audited, weaknesses identified.
- [x] Phase 1 complete: Formal requirement specification documented in `REQUIREMENT_AUDIT.md`.
- [ ] Phase 2: Literature-to-Software mapping formalized in `LITERATURE_TO_STRIDE.md`.
- [ ] Phase 3: Mathematical comparison of MCDM models (AHP vs. TOPSIS vs. Constrained WSM).
- [ ] Phase 4: Database schema normalization and missing data handling.
- [ ] Phase 5: Implementation of Two-Stage Scoring Engine with automated tests.
- [ ] Phase 6: Transparent explanation generation.
