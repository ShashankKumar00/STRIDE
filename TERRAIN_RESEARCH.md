# STRIDE — Terrain Traversability & Cost Modeling Research (Phase 8)

**Document Status:** Complete Phase 8 Research & Modeling Specification  
**Date:** October 2026  
**Author:** Antigravity AI Assistant  
**Target System:** STRIDE (Smart Terrain & Robotic Intelligence For Defense Engineering)  
**Objective:** Establish the scientific and mechanical foundation for transitioning STRIDE from binary categorical terrain matching to a continuous, vehicle-specific **Traversability and Terrain Cost Model** based on Papers 4 and 5.

---

## 1. Executive Summary

In current operational prototypes, terrain compatibility is often modeled as a binary check:
$$\text{Compatible} \in \{0, 100\}$$

However, literature on off-road military robotics (Thoresen et al. 2021, Ambrożkiewicz et al. 2026) demonstrates that **terrain traversability is a vehicle-specific continuum**. A vehicle with tracked mobility and 400 mm ground clearance traverses deep mud with relative ease, whereas a wheeled 4x4 UGV may suffer severe wheel sinkage, tire slippage, reduced velocity, or catastrophic immobilization.

This document establishes:
1. Physical and geotechnical parameters governing military terrain.
2. Vehicle mechanical attributes influencing off-road passability.
3. Mathematical formulation of the **STRIDE Traversability Index** ($T \in [0.0, 1.0]$).
4. Derivation of **Effective Speed Derating** and **Terrain Route Detour Factors**.
5. Practical data requirements for defense applications.

---

## 2. Geotechnical & Environmental Terrain Properties

Off-road defense terrain profiles are characterized by three fundamental physical dimensions:

### 2.1 Topographical Slope Gradient ($\theta$)
- Measured in degrees ($^\circ$) or percentage grade ($\tan \theta \times 100\%$).
- Influences vehicle longitudinal stability (pitch tipping limit) and requires tractive effort to overcome gravitational resistance:
  $$F_{\text{slope}} = m \cdot g \cdot \sin \theta$$

### 2.2 Soil Mechanics & Sinkage Resistance (Bekker Terramechanics)
- Governed by Bekker's pressure-sinkage equation for off-road soils:
  $$p = \left( \frac{k_c}{b} + k_\phi \right) z^n$$
  Where:
  - $p$: Contact pressure (kPa)
  - $b$: Wheel width or track width (m)
  - $z$: Sinkage depth (m)
  - $k_c, k_\phi, n$: Cohesion, friction, and sinkage exponents of the terrain.
- **Mud and Soft Soils:** High sinkage $z$, low shear strength, severe rolling resistance.
- **Sand / Desert:** High slip, low cohesion ($k_c \approx 0$), prone to trenching under excessive torque.
- **Paved / Urban:** Zero sinkage ($z \approx 0$), maximum traction coefficient ($\mu \approx 0.8\text{--}0.9$).

### 2.3 Macro-Roughness & Obstacle Density
- Surface obstacles (boulders, tree stumps, ruts, ditches, stairs).
- Obstacle height $h_{\text{obs}}$ relative to vehicle ground clearance $h_{gc}$. If $h_{\text{obs}} > h_{gc}$, high-centering (chassis hang-up) occurs.

---

## 3. Standardized Operating Terrain Classifications

STRIDE formalizes seven operational terrain classes:

| Terrain Class | Slope Range ($\theta$) | Surface Roughness ($\sigma$) | Soil Sinkage / Shear Risk | Friction Coeff ($\mu$) | Nominal Detour Factor ($\kappa$) |
|---|---|---|---|---|---|
| **Paved Road / Urban** | $0^\circ \text{--} 5^\circ$ | Minimal ($\sigma < 2\text{ cm}$) | Negligible | $0.85$ | $1.05$ |
| **Plain / Grassland** | $2^\circ \text{--} 12^\circ$ | Low ($\sigma \approx 5\text{ cm}$) | Low | $0.65$ | $1.15$ |
| **Desert / Sand** | $5^\circ \text{--} 25^\circ$ | Moderate ripples | High slip / Moderate sinkage | $0.40$ | $1.25$ |
| **Mud / Soft Ground** | $2^\circ \text{--} 15^\circ$ | High deformation | Extreme sinkage / Low shear | $0.35$ | $1.35$ |
| **Rugged / Mountainous / Rocky**| $10^\circ \text{--} 35^\circ$| Extreme boulders | Rigid obstacles / Tip risk | $0.55$ | $1.30$ |
| **Snow / Ice** | $2^\circ \text{--} 20^\circ$ | Variable crust | Extreme slip / Cold resistance | $0.25$ | $1.20$ |
| **Extreme Obstacles / Stairs** | $15^\circ \text{--} 45^\circ$| Step geometry | Geometric hang-up risk | $0.70$ | $1.40$ |

---

## 4. Vehicle Mobility Characteristics & Terramechanic Interaction

A vehicle's ability to negotiate a terrain profile depends directly on its physical running gear:

```
                      VEHICLE RUNNING GEAR
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
     TRACKED              WHEELED 6x6           WHEELED 4x4
  (e.g. MUNTRA, ZEUS)     (e.g. BRUTE)      (e.g. ECARS, Vrishabh)
         │                     │                     │
  • Low Ground Pressure • Moderate Pressure   • Higher Pressure
    (25-45 kPa)           (60-90 kPa)           (100-150 kPa)
  • Superior Mud/Snow   • Good Trench Span    • High Road Speed
  • High Obstacle Climb • Moderate Soft Soil  • Lower Mud Floatation
  • High Slope Traction • Efficient Transit   • High Power-to-Weight
```

### Key Vehicle Mobility Parameters:
1. **Mobility Class:**
   - `Tracked`: Best soft soil floatation and step climbing; lower road efficiency.
   - `Wheeled 6x6`: Intermediate floatation with trench-crossing capability.
   - `Wheeled 4x4`: High top speed on firm surfaces; higher risk of sinkage in deep mud.
2. **Effective Ground Clearance ($h_{gc}$):** Determines maximum negotiable obstacle height.
3. **Maximum Climbing Gradient ($\theta_{\max}$):** Engine torque and center-of-gravity tilt threshold.

---

## 5. Mathematical Formulation of the Traversability Index

For vehicle $v$ operating on terrain $\tau$, the **Traversability Index** $T(v, \tau) \in [0.0, 1.0]$ is formulated as a multi-factor product:

$$T(v, \tau) = \Phi_{\text{mobility}}(v, \tau) \cdot \Phi_{\text{slope}}(v, \tau) \cdot \Phi_{\text{clearance}}(v, \tau)$$

Where:

### 5.1 Mobility-Surface Compatibility Factor ($\Phi_{\text{mobility}}$):
Derived from the empirical mobility-soil interaction matrix:

| Mobility Class | Paved / Urban | Plain / Grass | Desert / Sand | Mud / Soft Ground | Rugged / Rocky | Snow / Ice | Extreme / Stairs |
|---|---|---|---|---|---|---|---|
| **Tracked** | $0.95$ | $1.00$ | $0.95$ | **$0.90$** | **$0.90$** | **$0.85$** | **$0.85$** |
| **Wheeled 6x6** | $1.00$ | $0.95$ | $0.80$ | $0.70$ | $0.75$ | $0.65$ | $0.45$ |
| **Wheeled 4x4** | **$1.00$** | $0.90$ | $0.70$ | $0.55$ | $0.65$ | $0.50$ | $0.30$ |

### 5.2 Slope Gradient Factor ($\Phi_{\text{slope}}$):
Given expected terrain slope $\theta$ and vehicle maximum slope capability $\theta_{\max}$:
$$\Phi_{\text{slope}}(v, \tau) = \begin{cases} 
1.0 & \text{if } \theta \le 0.5 \cdot \theta_{\max} \\
1.0 - \left( \frac{\theta - 0.5 \theta_{\max}}{0.5 \theta_{\max}} \right)^2 & \text{if } 0.5 \theta_{\max} < \theta \le \theta_{\max} \\
0.0 & \text{if } \theta > \theta_{\max} \quad (\text{Infeasible - Roll/Slide})
\end{cases}$$

### 5.3 Clearance-to-Obstacle Factor ($\Phi_{\text{clearance}}$):
Given expected terrain roughness obstacle height $h_{\text{obs}}$ and vehicle clearance $h_{gc}$:
$$\Phi_{\text{clearance}}(v, \tau) = \begin{cases}
1.0 & \text{if } h_{gc} \ge 1.5 \cdot h_{\text{obs}} \\
\frac{h_{gc}}{1.5 \cdot h_{\text{obs}}} & \text{if } 0.8 \cdot h_{\text{obs}} \le h_{gc} < 1.5 \cdot h_{\text{obs}} \\
0.0 & \text{if } h_{gc} < 0.8 \cdot h_{\text{obs}} \quad (\text{High-center hang-up})
\end{cases}$$

---

## 6. Operational Outputs of the Terrain Model

The Traversability Index $T(v, \tau)$ directly impacts operational mission metrics:

1. **Effective Operating Speed ($V_{\text{eff}}$):**
   $$V_{\text{eff}}(v, \tau) = V_{\max}(v) \times T(v, \tau)$$
   *Effect:* Vehicles operating in mud or rocky terrain travel slower than their advertised highway speed.

2. **Terrain Cost Factor ($C_{\text{terrain}}$):**
   $$C_{\text{terrain}} = \frac{1}{\max(T(v, \tau), 0.05)}$$
   *Effect:* Path planners use this cost to penalize paths cutting through hazardous or energy-draining terrain.

3. **Effective Travel Time ($t_{\text{effective}}$):**
   $$t_{\text{effective}} = \frac{D_{\text{actual}}}{V_{\text{eff}}} = \frac{D_{\text{nominal}} \cdot \kappa(\tau)}{V_{\max} \cdot T(v, \tau)}$$

---

## 7. Conclusion & Prototype Strategy (Phases 9 & 10)

This research provides the mathematical framework for:
- **Phase 9 (Terrain Prototype):** Building an isolated Python module `src/terrain/` implementing `calculate_traversability(vehicle, terrain_type)` and validating speed deratings.
- **Phase 10 (Route Planning):** Combining the terrain cost grid with an A* algorithm to simulate mission routes and verify physical transit feasibility.
