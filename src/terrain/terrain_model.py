# STRIDE — Terrain Model (Phase 9 Prototype)
# Defines standard terrain geotechnical profiles and mechanical constants

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TerrainProfile:
    name: str
    nominal_slope_deg: float
    max_slope_deg: float
    roughness_height_mm: float
    soil_sinkage_risk: str  # 'Low', 'Moderate', 'High', 'Extreme'
    friction_coefficient: float
    detour_factor: float  # Route distance expansion factor (kappa >= 1.0)
    description: str


# Canonical Defense Terrains
STANDARD_TERRAINS: Dict[str, TerrainProfile] = {
    "Paved Road / Urban": TerrainProfile(
        name="Paved Road / Urban",
        nominal_slope_deg=2.0,
        max_slope_deg=5.0,
        roughness_height_mm=10.0,
        soil_sinkage_risk="Low",
        friction_coefficient=0.85,
        detour_factor=1.05,
        description="Firm paved asphalt and concrete roads; zero sinkage, high traction."
    ),
    "Plain / Grassland": TerrainProfile(
        name="Plain / Grassland",
        nominal_slope_deg=5.0,
        max_slope_deg=12.0,
        roughness_height_mm=50.0,
        soil_sinkage_risk="Low",
        friction_coefficient=0.65,
        detour_factor=1.15,
        description="Firm open soil and rolling grass; moderate rolling resistance."
    ),
    "Desert / Sand": TerrainProfile(
        name="Desert / Sand",
        nominal_slope_deg=10.0,
        max_slope_deg=25.0,
        roughness_height_mm=100.0,
        soil_sinkage_risk="High",
        friction_coefficient=0.40,
        detour_factor=1.25,
        description="Loose sand dunes and desert flats; high slip and wheel trenching."
    ),
    "Mud / Soft Ground": TerrainProfile(
        name="Mud / Soft Ground",
        nominal_slope_deg=5.0,
        max_slope_deg=15.0,
        roughness_height_mm=120.0,
        soil_sinkage_risk="Extreme",
        friction_coefficient=0.35,
        detour_factor=1.35,
        description="Waterlogged marsh and deep mud; severe sinkage, demands low ground pressure."
    ),
    "Rugged / Mountainous / Rocky": TerrainProfile(
        name="Rugged / Mountainous / Rocky",
        nominal_slope_deg=15.0,
        max_slope_deg=35.0,
        roughness_height_mm=250.0,
        soil_sinkage_risk="Moderate",
        friction_coefficient=0.55,
        detour_factor=1.30,
        description="Boulders, talus, and broken ground; high tip risk and obstacle hang-up."
    ),
    "Snow / Ice": TerrainProfile(
        name="Snow / Ice",
        nominal_slope_deg=8.0,
        max_slope_deg=20.0,
        roughness_height_mm=80.0,
        soil_sinkage_risk="High",
        friction_coefficient=0.25,
        detour_factor=1.20,
        description="Sub-zero snowpack and icy inclines; low traction, risk of continuous slip."
    ),
    "Extreme Obstacles / Stairs / Confined Spaces": TerrainProfile(
        name="Extreme Obstacles / Stairs / Confined Spaces",
        nominal_slope_deg=25.0,
        max_slope_deg=45.0,
        roughness_height_mm=300.0,
        soil_sinkage_risk="Moderate",
        friction_coefficient=0.70,
        detour_factor=1.40,
        description="Urban stairs, rubble piles, and narrow trenches; steep steps and high center of gravity risk."
    )
}


def get_terrain_profile(terrain_name: str) -> TerrainProfile:
    """Retrieves standard terrain profile or defaults to Plain / Grassland."""
    return STANDARD_TERRAINS.get(terrain_name, STANDARD_TERRAINS["Plain / Grassland"])
