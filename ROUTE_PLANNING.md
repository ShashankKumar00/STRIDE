# STRIDE — Route Planning & Mission Feasibility Specification (Phase 10)

**Document Status:** Complete Phase 10 Specification & Algorithmic Design  
**Date:** October 2026  
**Author:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Formalize terrain-aware route planning, detour factor estimation, and mission transit feasibility for candidate UGVs based on Papers 4 and 5.

---

## 1. Executive Summary

A critical limitation identified in early STRIDE prototypes was the **Euclidean Straight-Line Assumption**:
$$\text{Actual Route Distance} = \text{Nominal Distance}$$

As demonstrated by Thoresen et al. (Paper 4) and Ambrożkiewicz et al. (Paper 5), off-road military vehicles rarely travel in straight Euclidean vectors. Terrain obstacles (boulders, slopes exceeding tipping limits, deep mud bogs, urban ruins) force the vehicle to detour, increasing the actual route distance by $10\%\text{--}40\%$. Furthermore, degraded off-road traversability reduces transit speed, increasing transit duration and battery consumption.

Phase 10 introduces:
1. An analytical **Terrain Detour Factor Formulation** ($\kappa(\tau)$) for rapid decision support.
2. A comparative evaluation of path planning algorithms ($A^*$, Hybrid $A^*$, $AD^*$).
3. A 2D terrain-cost grid path planner ($A^*$) providing simulated waypoint trajectories and route feasibility validation.

---

## 2. Algorithmic Trade-off Analysis

| Algorithm | Computational Complexity | Kinematic Feasibility | Terrain Cost Awareness | Suitability for STRIDE Desktop Tool |
|---|---|---|---|---|
| **Dijkstra** | $O(V \log V + E)$ | ❌ None (Holonomic grid) | ⚠️ Uniform cost | Low (Slow, uninformed search) |
| **Standard $A^*$** | $O(b^d)$ with heuristic | ❌ Grid cells (4/8 connected) | ✅ Full cell cost grid | **HIGH (Optimal for Decision Support)** |
| **Hybrid $A^*$ (Paper 4)** | $O(b^d)$ with continuous state | ✅ Non-holonomic ($x, y, \theta$) | ✅ Multi-layer traversability | High for execution; complex for initial selection |
| **Anytime $D^*$ ($AD^*$)** | High initialization | ⚠️ Grid-based | ✅ Dynamic map updates | Medium (Overkill for pre-mission UGV selection) |

### Algorithmic Recommendation for STRIDE:
- **Core Recommendation Phase:** Analytical **Terrain Detour Model** combined with continuous traversability speed derating.
- **Detailed Mission Feasibility Mode:** An **$A^*$ Terrain-Cost Grid Planner** running on a synthesized or ingested elevation/cost grid. This balances high computational responsiveness ($< 50$ ms) with defensible route estimation.

---

## 3. Mathematical Route Feasibility Formulation

### 3.1 Effective Route Distance ($D_{\text{effective}}$)
Given nominal direct distance $D_{\text{nominal}}$ and terrain detour factor $\kappa(\tau) \ge 1.0$:
$$D_{\text{effective}} = D_{\text{nominal}} \times \kappa(\tau)$$

### 3.2 Effective Transit Duration ($T_{\text{transit}}$)
Given vehicle maximum speed $V_{\max}$ and traversability index $T(v, \tau)$:
$$V_{\text{effective}} = V_{\max} \times \max(0.15, T(v, \tau))$$
$$T_{\text{transit}} = \frac{D_{\text{effective}}}{V_{\text{effective}}}$$

### 3.3 Route Feasibility Criterion:
A vehicle $v$ is declared **Route Feasible** if and only if:
$$(\text{Operating Range}(v) \ge D_{\text{effective}}) \land (T_{\text{transit}} \le \text{Max Mission Time}) \land (T(v, \tau) \ge 0.30)$$

---

## 4. Software Architecture (`src/planning/`)

```
src/planning/
├── __init__.py
└── route_planner.py
    ├── calculate_route_feasibility()  # Rapid analytical detour and duration audit
    └── simulate_grid_route()          # 2D A* search on synthetic terrain cost map
```

This structure keeps route planning cleanly decoupled from the core scoring engine, fulfilling Section 18 and Section 36 of the Master Architecture Specification.
