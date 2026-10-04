# STRIDE System Live Demonstration Script
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from databases.vehicle_database import VEHICLE_DATABASE
from databases.priority_weights import generate_weights
from databases.scoring_engine import rank_vehicles
from planning.route_planner import simulate_grid_route


def run_mission_demo(title, requirements, priorities):
    print("=" * 80)
    print(f"MISSION SCENARIO: {title.upper()}")
    print("=" * 80)
    print(f"  * Target Role:         {requirements['Mission Role']}")
    print(f"  * Operational Terrain: {requirements['Terrain']}")
    print(f"  * Mission Payload:     {requirements['Payload']} kg")
    print(f"  * Mission Distance:    {requirements['Operating Range']} km (Straight-line)")
    print(f"  * Time Window:         {requirements['Minimum Mission Time']}h to {requirements['Maximum Mission Time']}h (Deadline)")
    print("-" * 80)

    weights = generate_weights(priorities)
    results = rank_vehicles(VEHICLE_DATABASE, requirements, weights)

    feasible = results["feasible"]
    infeasible = results["infeasible"]
    derived = results["derived"]
    sensitivity = results.get("sensitivity", {})

    print(f"\n[STAGE 1 GATEKEEPER RESULTS]")
    print(f"Total Evaluated: {len(VEHICLE_DATABASE)} Indian UGVs")
    print(f"Qualified:       {len(feasible)} vehicles passed all hard physical & tactical constraints")
    print(f"Disqualified:    {len(infeasible)} vehicles failed mandatory constraints")

    if feasible:
        top = feasible[0]
        route = top.get("route_info", {})
        expl = top["explanation"]

        print("\n" + "#" * 80)
        print("[*] TOP RECOMMENDED VEHICLE")
        print("#" * 80)
        print(f"Vehicle:           {top['vehicle_name']} ({top.get('vehicle_id', 'N/A')})")
        print(f"Suitability Score: {top['final_score']:.2f}%")
        print(f"Manufacturer:      {top['details'].get('manufacturer', 'Unknown')}")
        print(f"Mobility Gear:     {top['details'].get('mobility_type', 'N/A')}")
        print(f"Max Speed:         {top['details'].get('max_speed_kmh', 0.0)} km/h")
        print(f"Operating Range:   {top['details'].get('operating_range_km', 'N/A')} km")
        print(f"Payload Capacity:  {top['details'].get('payload_capacity_kg', 'N/A')} kg")

        print("\nWHY RECOMMENDED (PHASE 6 EXPLAINABILITY):")
        print(f"  * {expl.get('summary', '')}")

        if expl.get("strengths"):
            print("\nKEY STRENGTHS:")
            for s in expl["strengths"]:
                print(f"  [+] {s}")

        if expl.get("weaknesses"):
            print("\nOPERATIONAL NOTICES / UNCERTAINTIES:")
            for w in expl["weaknesses"]:
                print(f"  [!] {w}")

        if route:
            print("\nTERRAIN & ROUTE FEASIBILITY (PHASE 10):")
            print(f"  * Nominal Distance:       {route['nominal_distance_km']:.1f} km")
            print(f"  * Terrain Detour Factor:   {route['detour_factor']:.2f}x (due to topography & obstacles)")
            print(f"  * Detour-Adjusted Route:   {route['effective_distance_km']:.1f} km")
            print(f"  * Off-Road Traversability: {route['traversability_index']:.2f} / 1.00")
            print(f"  * Effective Transit Speed: {route['effective_speed_kmh']:.1f} km/h")
            print(f"  * Estimated Transit Time:  {route['transit_duration_hours']:.2f} hours (Deadline: {route['deadline_hours']:.1f}h)")
            print(f"  * Route Feasibility:       {'PASS (Feasible)' if route['is_route_feasible'] else 'FAIL'}")

        print("\nQUALIFIED LEADERBOARD (STAGE 2 MCDM RANKING):")
        print(f"{'Rank':<6}{'Vehicle Name':<20}{'Suitability':<14}{'Effective Speed':<18}{'Mobility'}")
        print("-" * 75)
        for idx, v in enumerate(feasible, start=1):
            v_route = v.get("route_info", {})
            spd = f"{v_route.get('effective_speed_kmh', 0.0):.1f} km/h"
            print(f"#{idx:<5}{v['vehicle_name']:<20}{v['final_score']:>6.2f}%        {spd:<18}{v['details'].get('mobility_type')}")

        if sensitivity:
            print(f"\nDECISION ROBUSTNESS & SENSITIVITY (PHASE 7):")
            print(f"  * {sensitivity.get('summary', '')}")
            for sp in sensitivity.get("sensitive_parameters", []):
                print(f"    -> {sp}")

        # 2D A* Path Planning Simulation (Phase 10)
        sim = simulate_grid_route(top['details'], requirements['Terrain'], grid_size=(10, 10), seed=42)
        print(f"\n2D A* TERRAIN-COST PATH PLANNING SIMULATION (PHASE 10):")
        print(f"  * Grid Resolution: 10x10 cells | Obstacles encountered: {sim['obstacles_count']}")
        print(f"  * Route Search Success: {sim['success']}")
        print(f"  * Trajectory Waypoint Count: {sim['total_steps']} steps")
        print(f"  * Total Terrain Path Cost: {sim['total_cost']}")
        print("  * First 6 Path Waypoints: " + " -> ".join([str(p) for p in sim["path_waypoints"][:6]]) + " ... -> (9, 9)")

    print("\nDISQUALIFIED CANDIDATES (GATEKEEPER ELIMINATION):")
    for inf in infeasible:
        reasons = inf["explanation"].get("failed_constraints", [])
        print(f"  [X] {inf['vehicle_name']:<15} : {'; '.join(reasons)}")
    print("\n")


if __name__ == "__main__":
    # Demo 1: Rugged Mountain Reconnaissance Mission
    run_mission_demo(
        title="Rugged Mountain Reconnaissance (Northern Sector)",
        requirements={
            "Mission Role": "Reconnaissance",
            "Terrain": "Rugged / Mountainous / Rocky",
            "Payload": 25.0,
            "Operating Range": 15.0,
            "Minimum Mission Time": 0.5,
            "Maximum Mission Time": 2.0
        },
        priorities={
            "Mission Role": "Very High",
            "Terrain": "Very High",
            "Payload": "High",
            "Operating Range": "Very High",
            "Minimum Mission Time": "Low",
            "Maximum Mission Time": "High"
        }
    )

    # Demo 2: Heavy Logistics & Resupply Mission (Desert Sector)
    run_mission_demo(
        title="Heavy Logistics Resupply Mission (Western Desert Sector)",
        requirements={
            "Mission Role": "Logistics / Transport / Casualty Evacuation",
            "Terrain": "Desert / Sand",
            "Payload": 500.0,
            "Operating Range": 12.0,
            "Minimum Mission Time": 1.0,
            "Maximum Mission Time": 3.0
        },
        priorities={
            "Mission Role": "Very High",
            "Terrain": "High",
            "Payload": "Very High",
            "Operating Range": "High",
            "Minimum Mission Time": "Low",
            "Maximum Mission Time": "Medium"
        }
    )

    # Demo 3: Natural Language Mission Narrative Parsing & High-Altitude Tactical Evaluation
    print("=" * 80)
    print("NATURAL LANGUAGE MISSION NARRATIVE DEMO (PHASE 2 & 4 EXTENSIONS)")
    print("=" * 80)
    from mission.mission_parser import parse_mission_narrative
    narrative = (
        "Conduct high altitude reconnaissance and surveillance patrol in Ladakh at 16000 ft "
        "in sub-zero snow terrain, carrying 50 kg sensor payload with silent electric stealth "
        "and at least 8 km operator standoff within 3 hours."
    )
    print(f"INPUT FREE-TEXT NARRATIVE:\n  \"{narrative}\"\n")
    parsed = parse_mission_narrative(narrative)
    print("SMART PARSER EXTRACTION LOG:")
    for log in parsed["confidence_log"]:
        print(f"  [+] {log}")

    print("\nPARSED MISSION REQUIREMENTS FOR SCORING ENGINE:")
    print(f"  * Roles:       {parsed['roles']}")
    print(f"  * Terrain:     {parsed['terrain']}")
    print(f"  * Payload:     {parsed['payload_kg']} kg")
    print(f"  * Distance:    {parsed['operating_range_km']} km")
    print(f"  * Standoff:    {parsed['standoff_km']} km")
    print(f"  * Altitude:    {parsed['altitude_m']} m ASL")
    print(f"  * Temperature: {parsed['temperature_c']} deg C")
    print(f"  * Stealth:     {parsed['stealth_required']} (Silent Electric)")

    run_mission_demo(
        title="High-Altitude Himalayan Reconnaissance (Parsed from Natural Language)",
        requirements={
            "Mission Role": parsed["roles"][0],
            "Mission Roles": parsed["roles"],
            "Terrain": parsed["terrain"],
            "Payload": parsed["payload_kg"],
            "Operating Range": parsed["operating_range_km"],
            "Minimum Mission Time": parsed["min_time_hours"],
            "Maximum Mission Time": parsed["max_time_hours"],
            "Standoff Distance": parsed["standoff_km"],
            "Operational Altitude": parsed["altitude_m"],
            "Operating Temperature": parsed["temperature_c"],
            "Stealth Requirement": "Silent Electric Only" if parsed["stealth_required"] else "Standard (Any Propulsion)"
        },
        priorities={
            "Mission Role": "Very High",
            "Terrain": "Very High",
            "Payload": "High",
            "Operating Range": "High",
            "Minimum Mission Time": "Low",
            "Maximum Mission Time": "High"
        }
    )

