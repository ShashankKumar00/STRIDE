# STRIDE — Literature-to-Software Mapping (Phase 2)

**Document Status:** Complete Phase 2 Specification  
**Date:** October 2026  
**Auditor & Research Architect:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Map foundational defense robotic and multicriteria literature papers directly to STRIDE's software components, identifying current limitations, justified improvements, data requirements, implementation feasibility, and validation strategies.

---

## 1. Executive Summary & Conceptual Literature Hierarchy

The literature review across the five designated papers demonstrates that UGV mission selection cannot be treated as a collection of isolated features. Instead, as outlined in Section 15 of the Master Specification, the literature establishes a coherent decision hierarchy:

```
                    MISSION CONTEXT
                          │
                          ▼
                 USER REQUIREMENTS
                 (High-level mission needs: payload, route, deadline, role, terrain)
                          │
                          ▼
                  PRIORITY / WEIGHTS
                 (Saaty AHP, Expert judgment, Sensitivity awareness)
                          │
                          ▼
                 DECISION METHODOLOGY
                 (Two-Stage Gatekeeper + MCDM / TOPSIS / Normalization)
                          │
                          ▼
                VEHICLE CAPABILITIES
                 (Mechanical limits, speed, range, endurance, provenance)
                          │
                          ▼
               TERRAIN SUITABILITY
                 (Vehicle-terrain traversability index, non-binary modeling)
                          │
                          ▼
                 ROUTE FEASIBILITY
                 (Terrain-adjusted route cost, detour factors, obstacle bypass)
                          │
                          ▼
                 MISSION EXECUTION
                 (Simulation, runtime replanning, reporting)
```

This mapping translates each research paper into concrete software architecture decisions, while strictly respecting the **Non-Negotiable Rule (Section 40):** *Do not assume every idea in the literature must be implemented immediately; select only what is technically defensible, data-backed, and within project scope.*

---

## 2. Detailed Literature-to-Software Mapping

---

### MAPPING 1: Paper 1
**Citation:** Jan Furch and Adam Švásta (2022). *Use of Multicriteria Analysis in Unmanned Ground Vehicle Selection.*

| Mapping Dimension | Details |
|---|---|
| **Technical Concept** | Multicriteria Decision-Making (MCDM) formulation for UGV selection; parameter grouping (geometrical/passability characteristics, driving dynamics, special tactical capabilities); Saaty-based criteria weighting; power-function evaluation. |
| **Current STRIDE Equivalent** | Flat weighted-sum model in `src/databases/scoring_engine.py` with an arbitrary 1–5 integer priority scale in `src/databases/priority_weights.py`. |
| **Current Limitation** | Criteria are treated as a flat, unorganized list without hierarchical grouping. Weights are arbitrary unnormalized integers (1–5) lacking mathematical consistency checking. Scoring does not account for diminishing marginal utility or non-linear passability effects. |
| **Possible Improvement** | 1. Group criteria into logical defense dimensions: **Mobility Dynamics** (Speed, Range), **Mission Capability** (Role, Payload, Endurance), and **Environmental Passability** (Terrain compatibility).<br>2. Implement normalized Saaty/AHP weighting vectors ensuring $\sum w_j = 1.0$.<br>3. Introduce non-linear utility curves where additional capability beyond mission requirement yields diminishing marginal returns. |
| **Required Data** | Parameter groupings catalog; pairwise importance calibration matrix for defense operational profiles. |
| **Implementation Difficulty** | **Low to Medium** (Mathematical weighting matrices and grouped sum functions are straightforward to implement in Python). |
| **Validation Requirement** | Unit test verifying normalized weights sum to $1.00$; scenario comparison confirming that a vehicle with superior driving dynamics does not overpower a vehicle failing essential mission utility. |

---

### MAPPING 2: Paper 2
**Citation:** Mustafa Hamurcu and Tamer Eren (2020). *Selection of Unmanned Aerial Vehicles by Using Multicriteria Decision-Making for Defence.*

| Mapping Dimension | Details |
|---|---|
| **Technical Concept** | Two-stage MCDM framework combining Analytic Hierarchy Process (AHP) for objective weight determination with Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) for ranking; explicit classification of criteria into **Benefit** (higher is better) vs. **Cost** (lower is better); vector normalization; Sensitivity Analysis of weight fluctuations. |
| **Current STRIDE Equivalent** | Ad-hoc formula capping scores at $100\%$ (`min(V/R * 100, 100)`); single final percentage score; no distinction between cost/benefit criteria; no sensitivity testing. |
| **Current Limitation** | Cannot naturally handle cost criteria (e.g. vehicle weight, energy consumption rate, turnaround time). Lacks distance-to-ideal calculation (TOPSIS). User has no visibility into how fragile or robust the ranking is if a priority shifts slightly. |
| **Possible Improvement** | 1. Decouple weight generation from alternative ranking.<br>2. Classify criteria explicitly: Benefit (Payload reserve, Range reserve, Speed reserve, Endurance) vs. Cost (Fuel/energy consumption, Curb weight).<br>3. Implement TOPSIS Euclidean distance to Positive Ideal Solution ($A^+$) and Negative Ideal Solution ($A^-$).<br>4. Build automated **Sensitivity Analysis** module (Phase 7) to report ranking stability. |
| **Required Data** | Benefit/cost direction tags for each parameter schema attribute; normalization bounds; tolerance thresholds for sensitivity perturbation. |
| **Implementation Difficulty** | **Medium** (Standard linear algebra using Python/NumPy; requires clean tabular data structures). |
| **Validation Requirement** | Mathematical verification against established TOPSIS benchmarks; sensitivity test demonstrating ranking stability across $\pm 10\%$ weight perturbations. |

---

### MAPPING 3: Paper 3
**Citation:** Cüneyd Demir, Cengiz Eldem, and Mustafa Bozdemir (2024). *Unmanned Ground Vehicle Selection with Artificial Neural Networks.*

| Mapping Dimension | Details |
|---|---|
| **Technical Concept** | Machine learning selection engine mapping high-level user mission requirements to low-level engineering design parameters via a catalogue-trained feedforward Artificial Neural Network (ANN), evaluated via precision, recall, and F1-score. |
| **Current STRIDE Equivalent** | Internal derivation of required speed ($\text{Speed} = \text{Distance} / \text{Max Time}$) without prompting the user for speed; hiding internal formulas behind mission parameters. |
| **Current Limitation** | Currently conflates vehicle operating range with mission route distance. Lacks a formal derived-parameters module. The database contains only 10 records, rendering any supervised ML model completely untrainable and prone to severe overfitting/hallucination. |
| **Possible Improvement** | 1. Adopt the paper's core philosophy: **"Ask what the mission requires, not what the machine parameters are."**<br>2. Maintain a clear, deterministic Derived Parameters module (Phase 1/5).<br>3. **Explicitly defer ANN / Deep Learning** to future research until a verified dataset of $>500$ operational UGV mission scenarios exists. |
| **Required Data** | High-level mission requirement schema; deterministic mathematical conversion formulas for mission parameters. |
| **Implementation Difficulty** | **Low** for deterministic derived parameter module; **Unfeasible / Unjustified** for ANN due to extreme data sparsity (10 vehicles). |
| **Validation Requirement** | Mathematical validation of all derived formulas ($\text{Speed}_{\text{req}}$, $\text{Time}_{\text{est}}$, $\text{Endurance}_{\text{req}}$); edge-case boundary checks (e.g. division by zero protection). |

---

### MAPPING 4: Paper 4
**Citation:** Marius Thoresen, Niels Hygum Nielsen, Kim Mathiassen, and Kristin Y. Pettersen (2021). *Path Planning for UGVs Based on Traversability Hybrid A\*.*

| Mapping Dimension | Details |
|---|---|
| **Technical Concept** | Non-binary terrain modeling: terrain traversability is a vehicle-specific continuum based on vehicle physical characteristics (ground clearance, wheelbase, track/wheel type, slope tolerance) interacting with terrain roughness, gradient, and obstacles; path cost balances geometric distance against traversability difficulty using Hybrid A\*. |
| **Current STRIDE Equivalent** | Binary exact string matching in `score_terrain()` (`100` if string in vehicle terrain list else `0`). |
| **Current Limitation** | Complete failure of string matching due to taxonomy divergence (e.g. `"Road / Paved"` vs `"All Terrain"`). Assumes all capable vehicles cross terrain with identical ease. Ignores mechanical factors (tracked vs wheeled, ground clearance). |
| **Possible Improvement** | 1. **Immediate (Phase 4–5):** Standardize terrain taxonomy into a shared capability matrix mapping operational environments to vehicle mobility types.<br>2. **Intermediate (Phase 8):** Implement a semi-quantitative Traversability Index ($T \in [0.0, 1.0]$) accounting for mobility configuration (Tracked > 6x6 > 4x4 on soft mud/sand) and ground clearance.<br>3. **Long-Term (Phase 10):** Isolated Hybrid A\* route simulator. |
| **Required Data** | Standardized terrain matrix; vehicle mobility type (`Tracked`, `Wheeled 4x4`, `Wheeled 6x6`); ground clearance (mm); maximum climbing gradient (degrees). |
| **Implementation Difficulty** | **Low** for taxonomy harmonization; **Medium** for Traversability Index formula; **High** for full Hybrid A\* path planning. |
| **Validation Requirement** | Consistency test verifying that tracked heavy UGVs (e.g. MUNTRA) outperform light wheeled UGVs on extreme mud/sand, while wheeled UGVs retain speed advantages on paved roads. |

---

### MAPPING 5: Paper 5
**Citation:** Mateusz Ambrożkiewicz, Bonar Bartłomiej, and Tomasz Buratowski (2026). *Rough Terrain-Aware Mission Planning for Unmanned Ground Vehicles Using Geospatial Cost Maps and Local Replanning.* (SSRN Research Preprint).

| Mapping Dimension | Details |
|---|---|
| **Technical Concept** | Geospatial cost map generation from Digital Elevation Models (DEM) and point clouds; vehicle-specific route generation considering roll, pitch, and footprint; route feasibility verification; dynamic replanning during mission execution upon sensor detection of unmapped obstacles. |
| **Current STRIDE Equivalent** | Conceptual direct Euclidean line assumption ($\text{Distance} = \text{Operating Range}$ input). |
| **Current Limitation** | Assumes flat, unobstructed Euclidean routes. Real military routes require detours around unpassable topography, increasing actual travel distance by $15\%\text{--}40\%$. No geospatial or cost-grid capability. |
| **Possible Improvement** | 1. Introduce an analytical **Terrain Detour Factor** ($\kappa \ge 1.0$) to estimate effective route distance: $D_{\text{eff}} = D_{\text{nominal}} \times \kappa(\text{Terrain})$.<br>2. Clearly delineate the boundary between **STRIDE Core Decision Engine** (vehicle recommendation) and **Future Mission Execution Plugins** (GIS / LiDAR replanning).<br>3. Keep full GIS and sensor replanning as an external modular extension (Phase 10) rather than bloating the desktop decision prototype. |
| **Required Data** | Terrain-specific detour coefficients; elevation and surface type roughness factors. (Full GIS DEM rasters out of immediate scope). |
| **Implementation Difficulty** | **Low** for analytical Detour Factor; **Very High** for real-time geospatial cost maps and LiDAR replanning engines. |
| **Validation Requirement** | Route distance expansion validation; ensuring route feasibility checks disqualify UGVs whose range is insufficient once terrain detour factors are applied. |

---

## 3. Boundary Demarcation: Core STRIDE vs. Future Research

To ensure development remains defensible, rigorous, and within scope, the literature concepts are divided into two clear implementation tiers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 1: IMMEDIATE / CORE STRIDE SCOPE (Phases 1–7)                      │
│ - Two-Stage Decision Pipeline (Hard Feasibility Gatekeeper + MCDM)     │
│ - Normalized Weight Determination (Saaty / AHP Principles)              │
│ - Benefit vs. Cost Parameter Orientation (Paper 2)                      │
│ - Dimensionless Score Normalization & Outranking (TOPSIS / WSM)         │
│ - Mission Requirement to Engineering Parameter Derivation (Paper 3)     │
│ - Standardized Terrain-Mobility Matrix (Paper 4 Baseline)               │
│ - Analytical Terrain Route Expansion / Detour Factor (Paper 5 Baseline) │
│ - Result Explainability Engine & Sensitivity Analysis                   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 2: ADVANCED / FUTURE RESEARCH HORIZON (Phases 8–10)               │
│ - Artificial Neural Networks / Deep Learning (Deferred: data sparse)    │
│ - Full Hybrid A* Grid-Based Kinematic Path Planning                     │
│ - Digital Elevation Model (DEM) & Point Cloud GIS Ingestion             │
│ - Real-Time LiDAR Observation & Dynamic Map Replanning                  │
│ - Hardware-in-the-Loop UGV Telemetry Integration                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Synthesis of Actionable Improvements

| Literature Concept | Target Phase | Action to be Taken in STRIDE |
|---|---|---|
| **Two-Stage Feasibility Gatekeeper** | Phase 1 & 5 | Filter out vehicles failing hard constraints (Payload, Range, Role, Speed) before computing scores. |
| **Criteria Directionality (Benefit/Cost)** | Phase 3 & 5 | Formulate normalization where benefit criteria maximize and cost criteria minimize. |
| **Standardized Taxonomy & Matrix** | Phase 4 | Align UI dropdowns and DB records using a common canonical dictionary. |
| **Derived Mission Metrics** | Phase 1 & 5 | Encapsulate speed, transit time, and endurance reserve calculations in a dedicated module. |
| **Transparent Rationale Generation** | Phase 6 | Translate scoring deltas into plain-language military strengths, weaknesses, and margin of victory. |
| **Parameter Sensitivity Analysis** | Phase 7 | Test if ranking changes under $\pm 10\%\text{--}20\%$ priority variation to report stability. |
