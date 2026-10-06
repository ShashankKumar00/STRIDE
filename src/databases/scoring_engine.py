# Scoring Engine for STRIDE
# Implements Two-Stage Decision Framework (Phase 3 & 5)
# Stage 1: Deterministic Feasibility Gatekeeper Filter
# Stage 2: Normalized Multi-Criteria Preference Scoring & Ranking
# Result Explanation Generator (Phase 6)

def derive_mission_parameters(requirements):
    """
    Derives internal mission metrics from visible user inputs.
    
    Args:
        requirements (dict): User mission configuration dictionary.
        
    Returns:
        dict: Derived engineering parameters including required speed and route margins.
    """
    distance = float(requirements.get("Operating Range", requirements.get("Mission Distance", 0.0)))
    max_time = float(requirements.get("Maximum Mission Time", 0.0))
    min_time = float(requirements.get("Minimum Mission Time", 0.0))
    
    required_speed = (distance / max_time) if (max_time > 0 and distance > 0) else 0.0
    tactical_range_req = distance * 1.25  # 25% tactical detour/reserve margin
    
    return {
        "mission_distance": distance,
        "max_time": max_time,
        "min_time": min_time,
        "required_speed": required_speed,
        "tactical_range_req": tactical_range_req
    }


def evaluate_hard_constraints(vehicle, requirements, derived):
    """
    Stage 1 Gatekeeper: Evaluates non-negotiable physical and tactical constraints.
    
    Returns:
        tuple: (is_feasible: bool, failed_constraints: list of str)
    """
    failed = []
    
    # 1. Mission Role Compatibility
    req_roles = requirements.get("Mission Roles")
    if req_roles and isinstance(req_roles, list):
        supported_roles = vehicle.get("mission_roles", vehicle.get("role", []))
        normalized_supported = [r.strip().lower() for r in supported_roles]
        matched = [r for r in req_roles if r.strip().lower() in normalized_supported]
        if not matched:
            failed.append(f"Mission Role mismatch: vehicle does not support any of {req_roles}")
    else:
        req_role = requirements.get("Mission Role")
        if req_role:
            supported_roles = vehicle.get("mission_roles", vehicle.get("role", []))
            normalized_supported = [r.strip().lower() for r in supported_roles]
            if req_role.strip().lower() not in normalized_supported:
                failed.append(f"Mission Role mismatch: vehicle does not support '{req_role}'")
            
    # 2. Terrain Compatibility
    req_terrain = requirements.get("Terrain")
    if req_terrain:
        supported_terrains = vehicle.get("terrain_capabilities", vehicle.get("terrain", []))
        normalized_terrains = [t.strip().lower() for t in supported_terrains]
        req_norm = req_terrain.strip().lower()
        if (req_norm not in normalized_terrains) and ("all terrain" not in normalized_terrains):
            failed.append(f"Terrain incompatible: cannot operate on '{req_terrain}'")

    # 2b. Tactical Standoff / Control Range Check
    req_standoff = requirements.get("Standoff Distance")
    if req_standoff is not None:
        try:
            req_standoff_val = float(req_standoff)
            if req_standoff_val > 0:
                veh_standoff = vehicle.get("max_control_range_km")
                if veh_standoff is not None and veh_standoff < req_standoff_val:
                    failed.append(f"Insufficient control standoff: control range {veh_standoff} km < required {req_standoff_val} km")
        except (ValueError, TypeError):
            pass

    # 2c. Operational Altitude Check
    req_altitude = requirements.get("Operational Altitude")
    if req_altitude is not None:
        try:
            req_alt_val = float(req_altitude)
            if req_alt_val > 3000:
                veh_alt = vehicle.get("climate_altitude", {}).get("max_altitude_m_asl")
                if veh_alt is not None and veh_alt < req_alt_val:
                    failed.append(f"Exceeds altitude ceiling: vehicle rated for {veh_alt} m ASL < required {int(req_alt_val)} m ASL")
        except (ValueError, TypeError):
            pass

    # 2d. Operating Temperature Check
    req_temp = requirements.get("Operating Temperature")
    if req_temp is not None:
        try:
            req_t_val = float(req_temp)
            clim = vehicle.get("climate_altitude", {})
            min_t = clim.get("min_operating_temp_c", -20.0)
            max_t = clim.get("max_operating_temp_c", 50.0)
            if req_t_val < min_t or req_t_val > max_t:
                failed.append(f"Temperature outside operational envelope ({min_t:.0f}°C to {max_t:.0f}°C vs mission {req_t_val:.0f}°C)")
        except (ValueError, TypeError):
            pass

    # 2e. Stealth Profile Check
    if requirements.get("Stealth Requirement") == "Silent Electric Only" or requirements.get("Stealth Required") is True:
        prop = vehicle.get("stealth_profile", {}).get("propulsion_type", "")
        if "diesel" in prop.lower() or "ic engine" in prop.lower():
            failed.append("Acoustic/thermal stealth violation: platform uses internal combustion engine (signature too high)")

            
    # 3. Payload Capacity Check
    req_payload = float(requirements.get("Payload", 0.0))
    veh_payload = vehicle.get("payload_capacity_kg", vehicle.get("payload_capacity"))
    if veh_payload is None or veh_payload == "N/A" or veh_payload == "Mission-specific":
        # Missing payload: cannot verify safety for positive payload missions
        if req_payload > 0:
            failed.append(f"Payload unverified: capacity is unknown/mission-specific, cannot guarantee {req_payload} kg")
    else:
        try:
            if float(veh_payload) < req_payload:
                failed.append(f"Insufficient payload: capacity {veh_payload} kg < required {req_payload} kg")
        except (ValueError, TypeError):
            failed.append("Invalid payload specification in vehicle database")
            
    # 4. Operating Range Check
    distance = derived["mission_distance"]
    veh_range = vehicle.get("operating_range_km", vehicle.get("operating_range"))
    if veh_range is None or veh_range == "N/A":
        failed.append(f"Range unverified: vehicle range is unknown, cannot verify {distance} km mission")
    else:
        try:
            if float(veh_range) < distance:
                failed.append(f"Insufficient range: operating range {veh_range} km < mission distance {distance} km")
        except (ValueError, TypeError):
            failed.append("Invalid range specification in vehicle database")
            
    # 5. Speed / Time Ceiling Check
    req_speed = derived["required_speed"]
    veh_speed = vehicle.get("max_speed_kmh", vehicle.get("max_speed", 0.0))
    try:
        veh_speed = float(veh_speed)
        if veh_speed < req_speed:
            failed.append(f"Insufficient speed: max speed {veh_speed} km/h cannot beat deadline ({req_speed:.1f} km/h needed)")
    except (ValueError, TypeError):
        failed.append("Invalid speed specification in vehicle database")

    return (len(failed) == 0), failed


def score_capability(vehicle_value, required_value):
    """
    Standard benefit score capped at 100% per Master Specification (Section 7 & 30).
    """
    if required_value <= 0:
        return 100.0
    if vehicle_value is None or vehicle_value == "N/A":
        return None
    try:
        val = float(vehicle_value)
        req = float(required_value)
    except (ValueError, TypeError):
        return None
    return min((val / req) * 100.0, 100.0)


def score_mission_time(mission_distance, vehicle_speed, min_time, max_time):
    """
    Evaluates mission duration compliance. Fast completion is not penalized
    unless a positive minimum loiter time is explicitly required.
    """
    if mission_distance <= 0 or vehicle_speed <= 0 or max_time <= 0:
        return 0.0
    
    estimated_time = mission_distance / vehicle_speed
    
    # Within valid window
    if min_time <= estimated_time <= max_time:
        return 100.0
    
    # Exceeded deadline
    if estimated_time > max_time:
        excess = estimated_time - max_time
        return max(0.0, min(100.0, (max_time / (max_time + excess)) * 100.0))
        
    # Completed earlier than min_time: only penalize if min_time > 0 and loiter mandatory
    if min_time > 0 and estimated_time < min_time:
        diff = min_time - estimated_time
        return max(0.0, min(100.0, (min_time / (min_time + diff)) * 100.0))
        
    return 100.0


def calculate_vehicle_score(vehicle, requirements, weights, derived):
    """
    Stage 2 Preference Scoring for Feasible Vehicles.
    
    Computes normalized parameter scores, handles missing data neutrally,
    and calculates weighted suitability score.
    """
    scores = {}
    applicable_weights = {}
    
    # 1. Mission Role Score (100% for feasible vehicles)
    scores["Mission Role"] = 100.0
    applicable_weights["Mission Role"] = weights.get("Mission Role", 3.0)
    
    # 2. Terrain Compatibility Score (100% for feasible vehicles)
    scores["Terrain"] = 100.0
    applicable_weights["Terrain"] = weights.get("Terrain", 3.0)
    
    # 3. Payload Score
    veh_payload = vehicle.get("payload_capacity_kg", vehicle.get("payload_capacity"))
    p_score = score_capability(veh_payload, requirements.get("Payload", 0.0))
    if p_score is not None:
        scores["Payload"] = p_score
        applicable_weights["Payload"] = weights.get("Payload", 3.0)
    else:
        scores["Payload"] = 100.0  # Neutral treatment for feasible
        applicable_weights["Payload"] = weights.get("Payload", 3.0) * 0.5  # Lower weight on uncertainty
        
    # 4. Operating Range Score
    veh_range = vehicle.get("operating_range_km", vehicle.get("operating_range"))
    r_score = score_capability(veh_range, derived["mission_distance"])
    if r_score is not None:
        scores["Operating Range"] = r_score
        applicable_weights["Operating Range"] = weights.get("Operating Range", 3.0)
    else:
        scores["Operating Range"] = 100.0
        applicable_weights["Operating Range"] = weights.get("Operating Range", 3.0) * 0.5
        
    # 5. Mission Time Window Score
    veh_speed = float(vehicle.get("max_speed_kmh", vehicle.get("max_speed", 0.0)))
    t_score = score_mission_time(
        derived["mission_distance"],
        veh_speed,
        derived["min_time"],
        derived["max_time"]
    )
    scores["Mission Time"] = t_score
    time_weight = (weights.get("Minimum Mission Time", 3.0) + weights.get("Maximum Mission Time", 3.0)) / 2.0
    applicable_weights["Mission Time"] = time_weight
    
    # 6. Internal Speed Margin Score
    req_speed = derived["required_speed"]
    s_score = score_capability(veh_speed, req_speed)
    scores["Internal Speed"] = s_score if s_score is not None else 0.0
    applicable_weights["Internal Speed"] = weights.get("Maximum Mission Time", 3.0)
    
    # 7. Endurance Persistence Score
    veh_endurance = vehicle.get("endurance_hours", vehicle.get("endurance"))
    estimated_time = (derived["mission_distance"] / veh_speed) if veh_speed > 0 else 1.0
    e_score = score_capability(veh_endurance, estimated_time)
    if e_score is not None:
        scores["Endurance"] = e_score
        applicable_weights["Endurance"] = weights.get("Endurance", 3.0)
    else:
        # Unknown endurance: excluded from weight so candidate is not unfairly penalized
        scores["Endurance"] = None
        
    # Aggregate weighted score
    weighted_sum = 0.0
    total_weight = 0.0
    for param, score in scores.items():
        if score is not None and param in applicable_weights:
            w = applicable_weights[param]
            weighted_sum += score * w
            total_weight += w
            
    final_score = (weighted_sum / total_weight) if total_weight > 0 else 0.0
    return final_score, scores


def generate_explanation(vehicle, scores, is_feasible, failed_constraints, requirements, derived):
    """
    Phase 6: Generates transparent, data-driven plain-text explanation for the recommendation.
    """
    if not is_feasible:
        return {
            "status": "Infeasible",
            "summary": "Vehicle cannot safely execute this mission.",
            "failed_constraints": failed_constraints,
            "strengths": [],
            "weaknesses": failed_constraints
        }
        
    strengths = []
    weaknesses = []
    
    veh_payload = vehicle.get("payload_capacity_kg")
    req_payload = requirements.get("Payload", 0.0)
    if veh_payload is not None and veh_payload >= req_payload * 1.5:
        strengths.append(f"Generous payload capacity ({veh_payload} kg vs {req_payload} kg required)")
    elif veh_payload is not None:
        strengths.append(f"Meets payload requirement ({veh_payload} kg)")
        
    veh_range = vehicle.get("operating_range_km")
    distance = derived["mission_distance"]
    if veh_range is not None and veh_range >= distance * 2.0:
        strengths.append(f"High range reserve ({veh_range} km vs {distance} km mission)")
    elif veh_range is not None:
        strengths.append(f"Sufficient operating range ({veh_range} km)")
        
    veh_speed = vehicle.get("max_speed_kmh", 0.0)
    req_speed = derived["required_speed"]
    if veh_speed >= req_speed * 1.5:
        strengths.append(f"High speed margin ({veh_speed} km/h vs {req_speed:.1f} km/h needed)")
        
    veh_endurance = vehicle.get("endurance_hours")
    if veh_endurance is not None:
        strengths.append(f"Documented endurance of {veh_endurance} hours")
    else:
        weaknesses.append("Endurance specification is unverified/unknown")

    # Tactical standoff & stealth insights
    veh_ctrl = vehicle.get("max_control_range_km")
    if veh_ctrl is not None and veh_ctrl >= 5.0:
        links = vehicle.get("control_link_types", [])
        primary_link = links[0].split(" (")[0] if links else "RF Link"
        strengths.append(f"Extended operator standoff ({veh_ctrl:.1f} km via {primary_link})")

    veh_alt = vehicle.get("climate_altitude", {}).get("max_altitude_m_asl", 0)
    if veh_alt >= 4500:
        strengths.append(f"High-altitude certified up to {veh_alt} m ASL (Himalayan / Ladakh rated)")

    prop = vehicle.get("stealth_profile", {}).get("propulsion_type", "")
    if "electric" in prop.lower() and "silent" in prop.lower():
        db = vehicle.get("stealth_profile", {}).get("acoustic_stealth_db_at_10m", 40.0)
        strengths.append(f"Silent electric propulsion (Acoustic level ~{db:.0f} dBA at 10m)")
    elif "diesel" in prop.lower():
        weaknesses.append("Internal combustion engine creates higher acoustic/thermal signature")
        
    summary = f"Strong multi-criteria match achieving high compatibility across mission role, terrain, and operational parameters."
    
    return {
        "status": "Feasible",
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "failed_constraints": []
    }



def rank_vehicles(vehicles, requirements, weights):
    """
    Executes the full Two-Stage STRIDE Decision Pipeline.
    
    1. Validates inputs & derives mission parameters.
    2. Filters vehicles via Stage 1 Gatekeeper.
    3. Scores feasible candidates via Stage 2 MCDM Preference Engine.
    4. Generates transparent explanations.
    5. Returns sorted feasible list and diagnostic infeasible list.
    """
    derived = derive_mission_parameters(requirements)
    
    feasible_results = []
    infeasible_results = []
    
    if not isinstance(vehicles, list):
        return feasible_results
        
    for vehicle in vehicles:
        is_feasible, failed_constraints = evaluate_hard_constraints(vehicle, requirements, derived)
        
        if is_feasible:
            final_score, scores = calculate_vehicle_score(vehicle, requirements, weights, derived)
            explanation = generate_explanation(vehicle, scores, True, [], requirements, derived)
            
            # Phase 10: Terrain Route Feasibility
            try:
                from planning.route_planner import calculate_route_feasibility
                route_info = calculate_route_feasibility(
                    vehicle,
                    requirements.get("Terrain", "Plain / Grassland"),
                    derived["mission_distance"],
                    derived["max_time"]
                )
            except Exception:
                route_info = {}
                
            feasible_results.append({
                "vehicle_id": vehicle.get("vehicle_id", "N/A"),
                "vehicle_name": vehicle.get("vehicle_name", "Unknown Vehicle"),
                "is_feasible": True,
                "final_score": final_score,
                "scores": scores,
                "explanation": explanation,
                "route_info": route_info,
                "details": vehicle
            })
        else:
            explanation = generate_explanation(vehicle, {}, False, failed_constraints, requirements, derived)
            infeasible_results.append({
                "vehicle_id": vehicle.get("vehicle_id", "N/A"),
                "vehicle_name": vehicle.get("vehicle_name", "Unknown Vehicle"),
                "is_feasible": False,
                "final_score": 0.0,
                "scores": {},
                "explanation": explanation,
                "details": vehicle
            })
            
    # Sort feasible descending by score
    feasible_results.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Phase 7: Sensitivity Analysis
    sensitivity = perform_sensitivity_analysis(vehicles, requirements, weights, feasible_results)

    # Phase 8: Adaptive Trade-Off Analysis (Fallback when 0 candidates meet 100% hard constraints)
    compromise_results = []
    if not feasible_results and infeasible_results:
        compromise_results = evaluate_compromise_candidates(vehicles, requirements, weights, derived, infeasible_results)
    
    # Return feasible results with metadata attached
    return {
        "feasible": feasible_results,
        "compromise": compromise_results,
        "infeasible": infeasible_results,
        "derived": derived,
        "sensitivity": sensitivity
    }


def evaluate_compromise_candidates(vehicles, requirements, weights, derived, infeasible_results):
    """
    Phase 8: Adaptive Trade-Off & Compromise Analysis.
    When no platform achieves 100% compliance with strict gatekeepers, evaluates
    partial compliance, scores closest near-miss platforms, and articulates specific
    operational concessions / tactical trade-offs needed to accomplish the mission.
    """
    try:
        from planning.route_planner import calculate_route_feasibility
    except Exception:
        calculate_route_feasibility = None

    compromise_candidates = []
    req_payload = float(requirements.get("Payload", 0.0))
    req_range = derived.get("mission_distance", 0.0)
    req_standoff = float(requirements.get("Standoff Distance") or 0.0)
    req_terrain = requirements.get("Terrain", "")
    req_roles = requirements.get("Mission Roles") or [requirements.get("Mission Role", "")]
    if isinstance(req_roles, str):
        req_roles = [req_roles]
    req_stealth = requirements.get("Stealth Requirement", "")
    req_alt = float(requirements.get("Operational Altitude") or 0.0)

    for item in infeasible_results:
        vehicle = item["details"]
        failed_reasons = item["explanation"].get("failed_constraints", [])
        
        # Base scoring
        base_score, cat_scores = calculate_vehicle_score(vehicle, requirements, weights, derived)
        
        # Approximate total criteria evaluated
        total_criteria = 5
        if req_standoff > 0:
            total_criteria += 1
        if req_alt > 3000:
            total_criteria += 1
        if req_stealth:
            total_criteria += 1
        if requirements.get("Operating Temperature") is not None:
            total_criteria += 1
            
        met_count = max(0, total_criteria - len(failed_reasons))
        compliance_ratio = max(0.15, met_count / total_criteria)
        compliance_text = f"{int(compliance_ratio * 100)}% ({met_count}/{total_criteria} Met)"
        
        strengths_met = []
        compromises_needed = []
        deductions = 0.0
        
        # 1. Payload
        veh_payload = vehicle.get("payload_capacity_kg")
        try:
            veh_payload_val = float(veh_payload) if veh_payload is not None else 0.0
        except (ValueError, TypeError):
            veh_payload_val = 0.0
            
        if veh_payload_val >= req_payload and req_payload > 0:
            strengths_met.append(f"Payload Capacity: Rated for {veh_payload_val:.0f} kg (Satisfies required {req_payload:.0f} kg)")
        elif req_payload > 0:
            shortfall = req_payload - veh_payload_val
            deductions += min(18.0, (shortfall / req_payload) * 18.0)
            compromises_needed.append(f"Payload Limit: Rated for {veh_payload_val:.0f} kg vs {req_payload:.0f} kg required ({shortfall:.0f} kg shortfall) — Reduce sensor kit weight or split mission across tandem UGVs.")
            
        # 2. Operating Range
        veh_range = vehicle.get("operating_range_km")
        try:
            veh_range_val = float(veh_range) if veh_range is not None else 0.0
        except (ValueError, TypeError):
            veh_range_val = 0.0
            
        if veh_range_val >= req_range and req_range > 0:
            strengths_met.append(f"Operating Range: Rated for {veh_range_val:.0f} km (Exceeds mission distance {req_range:.0f} km)")
        elif req_range > 0:
            shortfall = req_range - veh_range_val
            deductions += min(16.0, (shortfall / req_range) * 16.0)
            compromises_needed.append(f"Transit Range: {veh_range_val:.0f} km available vs {req_range:.0f} km required ({shortfall:.0f} km deficit) — Requires intermediate battery depot or mobile recharging node.")

        # 3. Operator Standoff
        veh_standoff = vehicle.get("max_control_range_km")
        try:
            veh_standoff_val = float(veh_standoff) if veh_standoff is not None else 0.0
        except (ValueError, TypeError):
            veh_standoff_val = 0.0
            
        if req_standoff > 0:
            if veh_standoff_val >= req_standoff:
                strengths_met.append(f"Operator Standoff: Control range {veh_standoff_val:.0f} km meets requested {req_standoff:.0f} km standoff")
            else:
                shortfall = req_standoff - veh_standoff_val
                deductions += min(14.0, (shortfall / req_standoff) * 14.0)
                compromises_needed.append(f"Operator Standoff Link: Direct RF link is {veh_standoff_val:.0f} km vs {req_standoff:.0f} km requested ({shortfall:.0f} km deficit) — Deploy with forward relay station, mesh node, or tactical drone repeater.")

        # 4. Terrain
        veh_terrains = [t.strip().lower() for t in vehicle.get("terrain_capabilities", [])]
        if req_terrain.strip().lower() in veh_terrains or "all terrain" in veh_terrains:
            strengths_met.append(f"Terrain Mobility: Confirmed fully certified for '{req_terrain}'")
        else:
            deductions += 15.0
            compromises_needed.append(f"Terrain Certification: Platform not certified for '{req_terrain}' — Requires track cleat upgrades or ground-clearing escort.")

        # 5. Roles
        veh_roles = [r.strip().lower() for r in vehicle.get("mission_roles", [])]
        matched_roles = [r for r in req_roles if r.strip().lower() in veh_roles]
        if matched_roles:
            strengths_met.append(f"Mission Roles: Directly supports requested operational roles ({', '.join(matched_roles)})")
        else:
            deductions += 12.0
            compromises_needed.append(f"Mission Package: Dedicated role differs — Requires modular mission payload re-fit.")

        # 6. Stealth
        prop = vehicle.get("stealth_profile", {}).get("propulsion_type", "Standard")
        if req_stealth == "Silent Electric Only":
            if "electric" in prop.lower():
                strengths_met.append(f"Stealth Envelope: All-electric silent propulsion satisfies acoustic/thermal profile")
            else:
                deductions += 10.0
                compromises_needed.append(f"Acoustic/Thermal Signature: Utilizes {prop} powertrain (Higher acoustic/thermal signature than silent electric) — Operate with thermal shielding and standoff idling.")

        # 7. Altitude
        veh_alt = vehicle.get("climate_altitude", {}).get("max_altitude_m_asl", 3000)
        if req_alt > 3000:
            if veh_alt >= req_alt:
                strengths_met.append(f"Altitude Rating: Certified up to {veh_alt} m ASL (Meets {req_alt:.0f} m requirement)")
            else:
                deductions += 10.0
                compromises_needed.append(f"Altitude Ceiling: Certified to {veh_alt} m ASL vs {req_alt:.0f} m ASL requested — Requires cold-weather intake heating.")

        # Calculate final compromise score
        raw_tradeoff = (base_score * compliance_ratio * 0.7) + (85.0 * compliance_ratio * 0.3) - (deductions * 0.4)
        tradeoff_score = max(5.0, min(95.0, raw_tradeoff))
        
        # Primary shortfall for summary display
        primary_shortfall = compromises_needed[0].split("—")[0].strip() if compromises_needed else "Minor operational deviation"
        if len(primary_shortfall) > 36:
            primary_shortfall = primary_shortfall[:33] + "..."

        route_info = {}
        if calculate_route_feasibility:
            try:
                route_info = calculate_route_feasibility(
                    vehicle,
                    requirements.get("Terrain", "Plain / Grassland"),
                    derived["mission_distance"],
                    derived["max_time"]
                )
            except Exception:
                route_info = {}

        compromise_candidates.append({
            "vehicle_id": vehicle.get("vehicle_id", "N/A"),
            "vehicle_name": vehicle.get("vehicle_name", "Unknown Vehicle"),
            "is_feasible": False,
            "is_compromise": True,
            "final_score": tradeoff_score,
            "compliance_ratio": compliance_ratio,
            "compliance_text": compliance_text,
            "primary_shortfall": primary_shortfall,
            "scores": cat_scores,
            "route_info": route_info,
            "explanation": {
                "summary": f"Achieved highest partial multi-criteria compliance ({compliance_text}) among available defense platforms.",
                "strengths": strengths_met,
                "compromises": compromises_needed,
                "failed_constraints": failed_reasons
            },
            "details": vehicle
        })

    compromise_candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return compromise_candidates


def perform_sensitivity_analysis(vehicles, requirements, base_weights, feasible_results):
    """
    Phase 7: Evaluates recommendation robustness under priority perturbations.
    """
    if len(feasible_results) <= 1:
        return {
            "is_stable": True,
            "margin_of_victory": 0.0,
            "sensitive_parameters": [],
            "summary": "Single qualified candidate; recommendation is inherently stable."
        }
        
    top_name = feasible_results[0]["vehicle_name"]
    second_name = feasible_results[1]["vehicle_name"] if len(feasible_results) > 1 else ""
    margin = (feasible_results[0]["final_score"] - feasible_results[1]["final_score"]) if len(feasible_results) > 1 else 0.0
    sensitive = []
    
    test_params = ["Payload", "Operating Range", "Maximum Mission Time"]
    
    derived = derive_mission_parameters(requirements)
    
    for param in test_params:
        orig_w = base_weights.get(param, 3.0)
        
        for shift, label in [(2.0, "increased (+2)"), (-2.0, "decreased (-2)")]:
            test_w = dict(base_weights)
            test_w[param] = max(1.0, min(5.0, orig_w + shift))
            
            # Re-score feasible candidates under perturbed weight
            perturbed_scores = []
            for item in feasible_results:
                veh = item["details"]
                sc, _ = calculate_vehicle_score(veh, requirements, test_w, derived)
                perturbed_scores.append((veh["vehicle_name"], sc))
                
            perturbed_scores.sort(key=lambda x: x[1], reverse=True)
            if perturbed_scores and perturbed_scores[0][0] != top_name:
                sensitive.append(
                    f"Sensitive to {param} ({label}): {perturbed_scores[0][0]} ranks #1"
                )
                break
                
    is_stable = (len(sensitive) == 0)
    if is_stable:
        summary = f"Robust recommendation. {top_name} leads by a {margin:.1f}% margin of victory."
    else:
        summary = f"Recommendation sensitivity detected ({len(sensitive)} parameter shift(s) alter rank #1)."
        
    return {
        "is_stable": is_stable,
        "margin_of_victory": margin,
        "sensitive_parameters": sensitive,
        "summary": summary
    }