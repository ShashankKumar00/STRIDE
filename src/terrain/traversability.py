# STRIDE — Traversability Engine (Phase 9 Prototype)
# Calculates continuous, vehicle-specific traversability index and physical derating factors

from typing import Dict, Any
from terrain.terrain_model import get_terrain_profile, TerrainProfile


# Empirical mobility-soil compatibility factors (Paper 4 & 8)
MOBILITY_SURFACE_MATRIX = {
    "Tracked": {
        "Paved Road / Urban": 0.95,
        "Plain / Grassland": 1.00,
        "Desert / Sand": 0.95,
        "Mud / Soft Ground": 0.90,
        "Rugged / Mountainous / Rocky": 0.90,
        "Snow / Ice": 0.85,
        "Extreme Obstacles / Stairs / Confined Spaces": 0.85
    },
    "Wheeled 6x6": {
        "Paved Road / Urban": 1.00,
        "Plain / Grassland": 0.95,
        "Desert / Sand": 0.80,
        "Mud / Soft Ground": 0.70,
        "Rugged / Mountainous / Rocky": 0.75,
        "Snow / Ice": 0.65,
        "Extreme Obstacles / Stairs / Confined Spaces": 0.45
    },
    "Wheeled 4x4": {
        "Paved Road / Urban": 1.00,
        "Plain / Grassland": 0.90,
        "Desert / Sand": 0.70,
        "Mud / Soft Ground": 0.55,
        "Rugged / Mountainous / Rocky": 0.65,
        "Snow / Ice": 0.50,
        "Extreme Obstacles / Stairs / Confined Spaces": 0.30
    }
}

# Default maximum slope tolerances by mobility gear
DEFAULT_MAX_SLOPES = {
    "Tracked": 35.0,
    "Wheeled 6x6": 28.0,
    "Wheeled 4x4": 22.0
}


def calculate_traversability(vehicle: Dict[str, Any], terrain_name: str, slope_deg: float = None) -> Dict[str, Any]:
    """
    Computes continuous vehicle-terrain interaction metrics.
    
    Args:
        vehicle: Vehicle dictionary with mobility_type and speed specifications.
        terrain_name: Standardized terrain string.
        slope_deg: Optional operational terrain slope (defaults to terrain nominal slope).
        
    Returns:
        dict: Physical metrics including traversability_index, effective speed, and terrain cost.
    """
    profile: TerrainProfile = get_terrain_profile(terrain_name)
    mobility = vehicle.get("mobility_type", "Wheeled 4x4")
    
    # 1. Base Mobility-Soil Compatibility
    class_matrix = MOBILITY_SURFACE_MATRIX.get(mobility, MOBILITY_SURFACE_MATRIX["Wheeled 4x4"])
    phi_mobility = class_matrix.get(terrain_name, 0.70)
    
    # 2. Slope Gradient Evaluation
    operational_slope = slope_deg if slope_deg is not None else profile.nominal_slope_deg
    max_slope = DEFAULT_MAX_SLOPES.get(mobility, 22.0)
    
    if operational_slope <= 0.5 * max_slope:
        phi_slope = 1.0
    elif operational_slope <= max_slope:
        excess_ratio = (operational_slope - 0.5 * max_slope) / (0.5 * max_slope)
        phi_slope = max(0.2, 1.0 - (excess_ratio ** 2) * 0.7)
    else:
        # Exceeds physical climbing limit
        phi_slope = 0.05
        
    # 3. Aggregate Traversability Index T in [0.0, 1.0]
    traversability_index = round(phi_mobility * phi_slope, 4)
    
    # Passability threshold (T >= 0.30)
    is_passable = (traversability_index >= 0.30)
    
    # 4. Physical Deratings
    max_speed = float(vehicle.get("max_speed_kmh", 15.0))
    # Effective speed scales with traversability
    speed_factor = max(0.15, traversability_index)
    effective_speed = round(max_speed * speed_factor, 2)
    
    # Terrain traversal cost (higher cost for severe terrain)
    terrain_cost = round(1.0 / max(0.05, traversability_index), 2)
    
    # Energy consumption penalty multiplier (1.0 on road, up to 2.5 on mud/sand)
    energy_multiplier = round(1.0 + (1.0 - traversability_index) * 1.5, 2)
    
    return {
        "terrain_name": terrain_name,
        "mobility_type": mobility,
        "traversability_index": traversability_index,
        "is_passable": is_passable,
        "speed_factor": speed_factor,
        "effective_speed_kmh": effective_speed,
        "max_speed_kmh": max_speed,
        "terrain_cost": terrain_cost,
        "energy_multiplier": energy_multiplier,
        "detour_factor": profile.detour_factor,
        "friction_coefficient": profile.friction_coefficient
    }
