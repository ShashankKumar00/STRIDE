# STRIDE — Route Planning & Feasibility Engine (Phase 10 Prototype)
# Implements terrain-aware route feasibility, detour expansion, and 2D A* path planning

import heapq
import math
import random
from typing import Dict, Any, List, Tuple, Optional

from terrain.traversability import calculate_traversability
from terrain.terrain_model import get_terrain_profile


def calculate_route_feasibility(
    vehicle: Dict[str, Any],
    terrain_name: str,
    nominal_distance_km: float,
    max_time_hours: float
) -> Dict[str, Any]:
    """
    Evaluates physical route feasibility accounting for terrain detours and speed derating.
    
    Args:
        vehicle: Vehicle dictionary with speed and range specifications.
        terrain_name: Standardized terrain string.
        nominal_distance_km: Straight-line mission distance in km.
        max_time_hours: Operational deadline in hours.
        
    Returns:
        dict: Feasibility breakdown including effective distance, estimated transit time, and status.
    """
    trav = calculate_traversability(vehicle, terrain_name)
    detour_factor = trav["detour_factor"]
    
    # 1. Effective Route Distance
    effective_distance = round(nominal_distance_km * detour_factor, 2)
    
    # 2. Effective Speed & Transit Duration
    effective_speed = trav["effective_speed_kmh"]
    transit_duration_hours = round(effective_distance / effective_speed, 2) if effective_speed > 0 else 999.0
    
    # 3. Range Verification
    veh_range = vehicle.get("operating_range_km")
    has_range_data = veh_range is not None
    range_val = float(veh_range) if has_range_data else 0.0
    range_sufficient = (range_val >= effective_distance) if has_range_data else False
    
    # 4. Time Verification
    time_sufficient = (transit_duration_hours <= max_time_hours)
    
    # Overall Route Feasibility
    is_route_feasible = (
        trav["is_passable"] and
        time_sufficient and
        (range_sufficient if has_range_data else True)
    )
    
    reasons = []
    if not trav["is_passable"]:
        reasons.append(f"Terrain impassable for {vehicle.get('mobility_type')} gear (Traversability={trav['traversability_index']:.2f})")
    if not time_sufficient:
        reasons.append(f"Transit duration {transit_duration_hours:.1f}h exceeds deadline {max_time_hours:.1f}h")
    if has_range_data and not range_sufficient:
        reasons.append(f"Vehicle range {range_val:.1f} km insufficient for detour-adjusted route {effective_distance:.1f} km")
        
    return {
        "vehicle_name": vehicle.get("vehicle_name", "Unknown"),
        "terrain_name": terrain_name,
        "nominal_distance_km": nominal_distance_km,
        "detour_factor": detour_factor,
        "effective_distance_km": effective_distance,
        "traversability_index": trav["traversability_index"],
        "effective_speed_kmh": effective_speed,
        "transit_duration_hours": transit_duration_hours,
        "deadline_hours": max_time_hours,
        "is_route_feasible": is_route_feasible,
        "failure_reasons": reasons
    }


def simulate_grid_route(
    vehicle: Dict[str, Any],
    terrain_name: str,
    grid_size: Tuple[int, int] = (20, 20),
    start: Tuple[int, int] = (0, 0),
    goal: Optional[Tuple[int, int]] = None,
    obstacle_density: float = 0.15,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Simulates a 2D terrain-cost grid path search using the A* algorithm (Phase 10).
    
    Args:
        vehicle: Vehicle dictionary with mobility characteristics.
        terrain_name: Target terrain profile.
        grid_size: Dimensions of simulation grid (rows, cols).
        start: Starting cell coordinate (row, col).
        goal: Target cell coordinate (row, col). Defaults to bottom-right cell.
        obstacle_density: Probability of impassable obstacle per cell.
        seed: Deterministic random seed for reproducibility.
        
    Returns:
        dict: Path waypoints, path length, total cost, and execution status.
    """
    rows, cols = grid_size
    target_goal = goal if goal is not None else (rows - 1, cols - 1)
    trav = calculate_traversability(vehicle, terrain_name)
    base_cost = trav["terrain_cost"]
    
    # Generate deterministic obstacle map with start/goal safety margins
    rng = random.Random(seed)
    obstacles = set()
    protected_cells = {
        start, target_goal,
        (start[0] + 1, start[1]), (start[0], start[1] + 1), (start[0] + 1, start[1] + 1),
        (target_goal[0] - 1, target_goal[1]), (target_goal[0], target_goal[1] - 1), (target_goal[0] - 1, target_goal[1] - 1)
    }
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in protected_cells and rng.random() < obstacle_density:
                obstacles.add((r, c))
                
    # A* Algorithm Setup
    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        # Diagonal / Euclidean metric
        return math.hypot(a[0] - b[0], a[1] - b[1]) * base_cost

    open_set = []
    heapq.heappush(open_set, (0.0 + heuristic(start, target_goal), 0.0, start))
    
    came_from = {}
    g_score = {start: 0.0}
    
    # 8-connectivity (Orthogonal + Diagonal)
    directions = [
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
        (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)
    ]
    
    success = False
    
    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        
        if current == target_goal:
            success = True
            break
            
        for dr, dc, dist_weight in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            if neighbor in obstacles:
                continue
                
            tentative_g = current_g + (base_cost * dist_weight)
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, target_goal)
                came_from[neighbor] = current
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                
    # Reconstruct path
    path = []
    if success:
        curr = target_goal
        while curr in came_from:
            path.append(curr)
            curr = came_from[curr]
        path.append(start)
        path.reverse()
        
    return {
        "success": success,
        "grid_size": grid_size,
        "start": start,
        "goal": target_goal,
        "path_waypoints": path,
        "total_steps": len(path),
        "total_cost": round(g_score.get(target_goal, 0.0), 2) if success else None,
        "base_terrain_cost": base_cost,
        "obstacles_count": len(obstacles)
    }
