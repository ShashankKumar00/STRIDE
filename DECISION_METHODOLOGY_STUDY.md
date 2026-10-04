# STRIDE — Decision Methodology Study (Phase 3)

**Document Status:** Complete Phase 3 Study & Architectural Recommendation  
**Date:** October 2026  
**Author:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Compare candidate Multicriteria Decision-Making (MCDM) methodologies against the existing prototype scoring model, evaluate their mathematical properties and operational suitability, and recommend a single defensible decision framework for STRIDE.

---

## 1. Executive Summary

Selecting an Unmanned Ground Vehicle (UGV) for an Indian defence mission is a high-stakes decision involving conflicting quantitative specifications (payload, range, speed, endurance) and qualitative requirements (mission role, terrain clearance). 

In Phase 0, the audit identified that STRIDE's current scoring engine relies on an unconstrained, flat weighted sum where vehicles failing critical parameters (e.g. insufficient payload or mismatched role) still receive deceptive 60%–70% suitability scores.

This study systematically compares four decision methodologies:
1. **Current Linear Weighted Sum Model (WSM / SAW)**
2. **Pure Analytic Hierarchy Process (AHP - Saaty)**
3. **Pure TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)**
4. **Two-Stage Constrained Hybrid Framework (Gatekeeper Filter + Normalized TOPSIS / AHP Weighting)**

Based on data availability, mathematical validity, operational defense realism, and explainability, this study **recommends Methodology 4: Two-Stage Constrained Hybrid Framework**.

---

## 2. Comparative Evaluation of Decision Methodologies

---

### METHOD 1: Current Linear Weighted Sum Model (WSM / SAW)

#### Mathematical Formulation:
For alternative $i$ across $n$ criteria:
$$\text{Score}_i = \frac{\sum_{j=1}^n w_j \cdot S_{ij}}{\sum_{j=1}^n w_j}$$
Where $S_{ij} = \min\left(\frac{x_{ij}}{r_j} \times 100, 100\right)$ for benefit parameters, and $w_j \in \{1, 2, 3, 4, 5\}$.

#### Detailed Profile:
- **Input:** Raw vehicle specifications $x_{ij}$, mission requirements $r_j$, discrete priority weights $w_j$.
- **Output:** Scalar percentage compatibility score $\in [0\%, 100\%]$ and descending rank order.
- **Advantages:**
  - Extremely fast execution ($O(m \cdot n)$ complexity).
  - Intuitive to explain to non-technical users.
  - Requires minimal configuration.
- **Limitations:**
  - **Full Compensatory Bias:** Severe deficits on critical parameters (e.g., carrying 50 kg on a 500 kg mission) are compensated by surpluses on irrelevant parameters (e.g. excess speed).
  - **No Constraint Gatekeeper:** Unusable vehicles receive high overall scores.
  - **Artificial Capping Discontinuity:** Hard cap at $100\%$ destroys information about safety reserves and vehicle expansion margins.
  - **Unnormalized Weights:** Arbitrary integer scales (1–5) distort relative parameter importance.
  - **Inability to Model Cost Criteria:** Does not naturally account for parameters where lower is better (e.g., energy consumption, curb weight).
- **Data Requirements:** Basic vehicle parameter list and user priority selections.
- **Suitability for STRIDE:** **Low / Deficient** (Unacceptable for defence decision-making without major modification).

---

### METHOD 2: Pure Analytic Hierarchy Process (AHP - Saaty 1980)

#### Mathematical Formulation:
1. Construct pairwise comparison matrix $A = [a_{jk}]_{n \times n}$ using Saaty's 1–9 fundamental scale.
2. Determine priority vector $w$ by computing principal eigenvector:
   $$A w = \lambda_{\max} w$$
3. Verify Consistency Index ($CI$) and Consistency Ratio ($CR$):
   $$CI = \frac{\lambda_{\max} - n}{n - 1}, \quad CR = \frac{CI}{RI} < 0.10$$
4. Repeat pairwise comparisons for all $m$ alternatives across all $n$ criteria ($n \times \frac{m(m-1)}{2}$ comparisons).

#### Detailed Profile:
- **Input:** Pairwise subjective preference judgments between all criteria and between all candidate vehicles for each criterion.
- **Output:** Normalized global priority vector $\sum P_i = 1.0$ and consistency metric $CR$.
- **Advantages:**
  - Mathematically rigorous weighting methodology.
  - Explicit validation of decision-maker consistency ($CR < 0.1$).
  - Capable of structuring complex hierarchical objectives (e.g., Tactical, Logistics, Survivability).
- **Limitations:**
  - **Combinatorial Explosion for Alternatives:** For $m = 10$ vehicles and $n = 6$ criteria, the user or system must perform $6 \times \frac{10 \times 9}{2} = 270$ pairwise alternative comparisons per mission!
  - **Impractical for Operational Software:** A field military planner cannot fill out hundreds of pairwise comparisons during mission configuration.
  - **Susceptible to Rank Reversal:** Adding or removing an irrelevant vehicle can change the relative rank of other vehicles.
- **Data Requirements:** Extensive expert comparison matrices; continuous user input.
- **Suitability for STRIDE:** **High for Criterion Weighting**, but **Unviable for Direct Alternative Ranking**.

---

### METHOD 3: Pure TOPSIS (Hamurcu & Eren 2020)

#### Mathematical Formulation:
1. Construct decision matrix $X = [x_{ij}]_{m \times n}$.
2. Compute normalized decision matrix $R = [r_{ij}]$ using vector normalization:
   $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^m x_{kj}^2}}$$
3. Calculate weighted normalized decision matrix $V = [v_{ij}] = [w_j \cdot r_{ij}]$.
4. Determine Positive Ideal Solution ($A^+$) and Negative Ideal Solution ($A^-$):
   $$A^+ = \{ \max_i(v_{ij}) \mid j \in J_b \}, \quad A^- = \{ \min_i(v_{ij}) \mid j \in J_b \}$$
5. Calculate Euclidean separation distances $D_i^+$ and $D_i^-$:
   $$D_i^+ = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^+)^2}, \quad D_i^- = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^-)^2}$$
6. Calculate relative closeness to ideal solution:
   $$C_i^* = \frac{D_i^-}{D_i^+ + D_i^-} \quad (0 \le C_i^* \le 1)$$

#### Detailed Profile:
- **Input:** Objective performance matrix of candidate vehicles, criterion weights $w_j$, benefit/cost classification sets ($J_b, J_c$).
- **Output:** Closeness coefficient $C_i^* \in [0.0, 1.0]$ and ranked candidate list.
- **Advantages:**
  - Simultaneously minimizes distance to the best possible vehicle while maximizing distance from the worst.
  - Seamlessly handles both **Benefit criteria** (payload, range, speed) and **Cost criteria** (fuel consumption, cost, weight).
  - Dimensionless vector normalization eliminates unit mismatch issues (kg vs km vs hours).
  - Highly computationally efficient ($O(m \cdot n)$); no alternative pairwise comparisons required.
- **Limitations:**
  - **Lacks Hard Constraint Checking:** If evaluated directly on raw candidates, an UGV with zero payload could theoretically score moderately well if its range and speed are exceptional.
  - Relative closeness $C_i^*$ is relative to the candidate cohort rather than an absolute mission pass mark.
- **Data Requirements:** Tabular numeric candidate specifications and criteria weights.
- **Suitability for STRIDE:** **High**, but requires a front-end feasibility gatekeeper.

---

### METHOD 4: RECOMMENDED — Two-Stage Constrained Hybrid Framework
*(Gatekeeper Feasibility Filter + AHP-Weighted Normalized TOPSIS)*

```
┌────────────────────────────────────────────────────────┐
│               MISSION REQUIREMENTS INPUT               │
│ (Role, Terrain, Payload, Distance, Time Window, Prio)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│       STAGE 1: HARD FEASIBILITY GATEKEEPER             │
│                                                        │
│  - Role Compatibility: Vehicle must support role       │
│  - Terrain Compatibility: Vehicle must support terrain │
│  - Payload Threshold: Capacity >= Required Payload     │
│  - Range Threshold: Range >= Route Distance            │
│  - Speed Threshold: Max Speed >= Required Speed        │
└─────────────┬────────────────────────────┬─────────────┘
              │ Pass                       │ Fail
              ▼                            ▼
┌───────────────────────────────┐ ┌──────────────────────┐
│     FEASIBLE CANDIDATES       │ │ INFEASIBLE VEHICLES  │
│     (Eligible for Ranking)    │ │ (Disqualified with   │
└─────────────┬─────────────────┘ │  specific diagnosis) │
              │                   └──────────────────────┘
              ▼
┌────────────────────────────────────────────────────────┐
│       STAGE 2: MULTI-CRITERIA PREFERENCE RANKING       │
│                                                        │
│  1. Priority Weighting: Normalized AHP/Direct Weights  │
│  2. Benefit/Cost Formulation                           │
│  3. Vector Normalization & Distance-to-Ideal (TOPSIS)  │
│  4. Relative Closeness Suitability Score C_i*          │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│          EXPLAINABLE RECOMMENDATION ENGINE             │
│  - #1 Top Recommended UGV                              │
│  - Full Ranked Leaderboard                             │
│  - Strengths, Weaknesses, Safety Margins               │
│  - Sensitivity Stability Verification                  │
└────────────────────────────────────────────────────────┘
```

#### Detailed Profile:
- **Stage 1 (Deterministic Gatekeeper):** Partitions all catalog vehicles into `Feasible` and `Infeasible` cohorts using crisp physical and tactical thresholds. Disqualified vehicles are documented with clear engineering reasons (e.g. *"Disqualified: Payload 50 kg < Required 100 kg"*).
- **Stage 2 (MCDM Preference Engine):** Evaluates the feasible cohort using normalized multi-criteria analysis (TOPSIS). Weights are derived from user priorities and normalized ($\sum w_j = 1.0$).
- **Advantages:**
  - **Zero Compensatory Hazard:** Impossible vehicles are eliminated before any scoring occurs.
  - **Defensible Mathematics:** Combines deterministic engineering constraint satisfaction with proven MCDM optimization.
  - **Preserves Reserve Differentiation:** Does not truncate surplus capability at 100%; rewards vehicles providing superior tactical margins.
  - **Full Explainability:** Separates *why a vehicle is feasible* from *why it was preferred over other feasible vehicles*.
  - **Ready for Sensitivity Analysis:** Directly supports stability testing across varying priority weights.
- **Suitability for STRIDE:** **OPTIMAL (Recommended Choice).**

---

## 3. Comprehensive Comparison Matrix

| Evaluation Criteria | 1. Linear WSM (Current) | 2. Pure AHP | 3. Pure TOPSIS | 4. Two-Stage Hybrid (Recommended) |
|---|---|---|---|---|
| **Eliminates Infeasible Vehicles?** | ❌ No (Compensates) | ❌ No | ❌ No | ✅ **Yes (Guaranteed)** |
| **Handles Benefit & Cost Criteria?** | ❌ No (Ad-hoc) | ⚠️ Indirectly | ✅ Yes | ✅ **Yes** |
| **User Burden / Complexity** | ✅ Minimal | ❌ Extreme (270 queries)| ✅ Minimal | ✅ **Minimal** |
| **Normalization Soundness** | ❌ Flawed (Cap at 100) | ⚠️ Subjective scale | ✅ Vector norm | ✅ **Vector norm** |
| **Mathematical Defensibility** | ❌ Low | ✅ High | ✅ High | ✅ **Highest** |
| **Support for Sensitivity Testing** | ⚠️ Weak | ⚠️ Moderate | ✅ Strong | ✅ **Strongest** |
| **Transparent Rationale Output** | ❌ Percentage only | ⚠️ Weight vector only | ⚠️ Distance only | ✅ **Diagnostic + Ranking** |
| **Implementation Effort in Python** | Existing | High | Medium | **Medium** |

---

## 4. Final Recommendation & Implementation Specification

Antigravity formally recommends adopting **Methodology 4: Two-Stage Constrained Hybrid Framework** for STRIDE.

### Mathematical Parameters for Stage 2 (TOPSIS Engine):
1. **Payload Margin Criterion ($C_1$ - Benefit):**
   $$\text{Margin}_{\text{payload}} = \frac{\text{Vehicle Payload} - \text{Required Payload}}{\text{Required Payload}} + 1.0$$
2. **Range Reserve Criterion ($C_2$ - Benefit):**
   $$\text{Reserve}_{\text{range}} = \frac{\text{Vehicle Range} - \text{Mission Distance}}{\text{Mission Distance}} + 1.0$$
3. **Mission Promptness Criterion ($C_3$ - Benefit):**
   $$\text{Promptness} = \frac{\text{Vehicle Max Speed}}{\text{Required Speed}}$$
4. **Endurance Persistence Criterion ($C_4$ - Benefit):**
   $$\text{Persistence} = \frac{\text{Vehicle Endurance}}{\text{Estimated Mission Time}}$$
5. **Terrain Traversability Metric ($C_5$ - Benefit):**
   Categorical compatibility score derived from the normalized mobility-terrain matrix.

### Weight Derivation Policy:
User priority selections (`Very High`: 5, `High`: 4, `Medium`: 3, `Low`: 2, `Very Low`: 1) are normalized to sum to unity:
$$w_j = \frac{p_j}{\sum_{k=1}^n p_k}, \quad \sum_{j=1}^n w_j = 1.00$$

This methodology directly resolves every limitation identified during the Phase 0 audit and establishes a sound foundation for Phase 4 (Data Schema) and Phase 5 (Scoring Engine implementation).
