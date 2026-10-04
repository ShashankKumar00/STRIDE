import unittest
import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from databases.vehicle_database import VEHICLE_DATABASE
from databases.priority_weights import generate_weights, normalize_weights
from databases.scoring_engine import (
    derive_mission_parameters,
    evaluate_hard_constraints,
    score_capability,
    score_mission_time,
    calculate_vehicle_score,
    rank_vehicles
)


class TestScoringEngine(unittest.TestCase):

    def setUp(self):
        self.sample_vehicle = {
            "vehicle_id": "TEST-001",
            "vehicle_name": "TestUGV",
            "mission_roles": ["Reconnaissance", "Surveillance"],
            "terrain_capabilities": ["Paved Road / Urban", "Rugged / Mountainous / Rocky"],
            "payload_capacity_kg": 100.0,
            "max_speed_kmh": 20.0,
            "operating_range_km": 50.0,
            "endurance_hours": 6.0
        }

    # 1. Score Calculation Tests per Master Specification Section 30 & 31
    def test_score_exceeds_requirement(self):
        """Test: Vehicle exceeds requirement -> Expected: Full satisfaction, not > 100%"""
        score = score_capability(vehicle_value=150.0, required_value=100.0)
        self.assertEqual(score, 100.0)

    def test_score_exactly_meets_requirement(self):
        """Test: Vehicle exactly meets requirement -> Expected: Full satisfaction (100%)"""
        score = score_capability(vehicle_value=100.0, required_value=100.0)
        self.assertEqual(score, 100.0)

    def test_score_below_requirement(self):
        """Test: Vehicle below requirement -> Expected: Linear ratio"""
        score = score_capability(vehicle_value=50.0, required_value=100.0)
        self.assertAlmostEqual(score, 50.0)

    def test_missing_data_neutral_handling(self):
        """Test: None or N/A should return None, not crash or return synthetic 0"""
        score_none = score_capability(vehicle_value=None, required_value=100.0)
        self.assertIsNone(score_none)
        score_na = score_capability(vehicle_value="N/A", required_value=100.0)
        self.assertIsNone(score_na)

    # 2. Hard Constraint Gatekeeper Tests
    def test_constraint_role_mismatch_infeasible(self):
        """Test: Vehicle fails mission role -> Expected: Infeasible"""
        req = {"Mission Role": "CBRN Reconnaissance", "Terrain": "Paved Road / Urban", "Payload": 50.0}
        derived = derive_mission_parameters({"Operating Range": 10.0, "Maximum Mission Time": 2.0})
        is_feasible, failed = evaluate_hard_constraints(self.sample_vehicle, req, derived)
        self.assertFalse(is_feasible)
        self.assertTrue(any("Mission Role mismatch" in f for f in failed))

    def test_constraint_terrain_incompatible_infeasible(self):
        """Test: Vehicle fails terrain -> Expected: Infeasible"""
        req = {"Mission Role": "Reconnaissance", "Terrain": "Desert / Sand", "Payload": 50.0}
        derived = derive_mission_parameters({"Operating Range": 10.0, "Maximum Mission Time": 2.0})
        is_feasible, failed = evaluate_hard_constraints(self.sample_vehicle, req, derived)
        self.assertFalse(is_feasible)
        self.assertTrue(any("Terrain incompatible" in f for f in failed))

    def test_constraint_insufficient_payload_infeasible(self):
        """Test: Vehicle payload capacity < required payload -> Expected: Infeasible"""
        req = {"Mission Role": "Reconnaissance", "Terrain": "Paved Road / Urban", "Payload": 150.0}
        derived = derive_mission_parameters({"Operating Range": 10.0, "Maximum Mission Time": 2.0})
        is_feasible, failed = evaluate_hard_constraints(self.sample_vehicle, req, derived)
        self.assertFalse(is_feasible)
        self.assertTrue(any("Insufficient payload" in f for f in failed))

    def test_constraint_insufficient_range_infeasible(self):
        """Test: Vehicle range < mission distance -> Expected: Infeasible"""
        req = {"Mission Role": "Reconnaissance", "Terrain": "Paved Road / Urban", "Payload": 50.0}
        derived = derive_mission_parameters({"Operating Range": 60.0, "Maximum Mission Time": 5.0})
        is_feasible, failed = evaluate_hard_constraints(self.sample_vehicle, req, derived)
        self.assertFalse(is_feasible)
        self.assertTrue(any("Insufficient range" in f for f in failed))

    def test_constraint_insufficient_speed_infeasible(self):
        """Test: Vehicle speed cannot beat deadline -> Expected: Infeasible"""
        req = {"Mission Role": "Reconnaissance", "Terrain": "Paved Road / Urban", "Payload": 50.0}
        # 50 km in 1 hour requires 50 km/h; vehicle max speed is 20 km/h
        derived = derive_mission_parameters({"Operating Range": 50.0, "Maximum Mission Time": 1.0})
        is_feasible, failed = evaluate_hard_constraints(self.sample_vehicle, req, derived)
        self.assertFalse(is_feasible)
        self.assertTrue(any("Insufficient speed" in f for f in failed))

    # 3. Priority Weighting & Normalization Tests
    def test_weight_normalization(self):
        """Test: Normalized weights must sum to 1.0"""
        prio = {
            "Payload": "High",
            "Terrain": "Very High",
            "Mission Role": "Medium",
            "Operating Range": "Low",
            "Maximum Mission Time": "Very Low"
        }
        weights = generate_weights(prio)
        norm_weights = normalize_weights(weights)
        self.assertAlmostEqual(sum(norm_weights.values()), 1.0)

    # 4. Realistic Defense Mission Scenario Tests (Section 31)
    def test_scenario_a_reconnaissance_rugged(self):
        """
        Scenario A: Reconnaissance mission in rugged terrain, 10 km distance, 1 hour deadline, 10 kg payload.
        Expected: Vehicles with Reconnaissance role and Rugged terrain support should be feasible.
        """
        req = {
            "Mission Role": "Reconnaissance",
            "Terrain": "Rugged / Mountainous / Rocky",
            "Payload": 10.0,
            "Operating Range": 10.0,
            "Minimum Mission Time": 0.5,
            "Maximum Mission Time": 1.5
        }
        prio = {k: "Medium" for k in req}
        weights = generate_weights(prio)
        
        result = rank_vehicles(VEHICLE_DATABASE, req, weights)
        
        # Verify result structure
        self.assertIn("feasible", result)
        self.assertIn("infeasible", result)
        self.assertTrue(len(result["feasible"]) > 0)
        
        feasible_names = [v["vehicle_name"] for v in result["feasible"]]
        # Vrishabh supports Reconnaissance, Rugged terrain, 150kg payload, 100km range, 50km/h speed
        self.assertIn("Vrishabh", feasible_names)
        
        # Top vehicle should have explanation attached
        top_ugv = result["feasible"][0]
        self.assertIn("explanation", top_ugv)
        self.assertTrue(len(top_ugv["explanation"]["strengths"]) > 0)

    def test_scenario_b_cbrn_mission(self):
        """
        Scenario B: CBRN Reconnaissance in Urban/Paved road.
        Expected: MUNTRA-N should be qualified; others lacking CBRN role must be infeasible.
        """
        req = {
            "Mission Role": "CBRN Reconnaissance",
            "Terrain": "Paved Road / Urban",
            "Payload": 0.0,
            "Operating Range": 10.0,
            "Minimum Mission Time": 1.0,
            "Maximum Mission Time": 2.0
        }
        prio = {k: "Medium" for k in req}
        weights = generate_weights(prio)
        
        result = rank_vehicles(VEHICLE_DATABASE, req, weights)
        feasible_names = [v["vehicle_name"] for v in result["feasible"]]
        
        self.assertIn("MUNTRA-N", feasible_names)
        # Vehicles without CBRN must be in infeasible list
        infeasible_names = [v["vehicle_name"] for v in result["infeasible"]]
        self.assertIn("Mooshak", infeasible_names)
        self.assertIn("BRUTE", infeasible_names)

    def test_scenario_c_heavy_logistics(self):
        """
        Scenario C: Heavy logistics resupply (500 kg payload) over 15 km plain.
        Expected: ZEUS (1500 kg) must qualify; vehicles with payload < 500 kg must be infeasible.
        """
        req = {
            "Mission Role": "Logistics / Transport / Casualty Evacuation",
            "Terrain": "Plain / Grassland",
            "Payload": 500.0,
            "Operating Range": 15.0,
            "Minimum Mission Time": 1.0,
            "Maximum Mission Time": 3.0
        }
        prio = {k: "Medium" for k in req}
        weights = generate_weights(prio)
        
        result = rank_vehicles(VEHICLE_DATABASE, req, weights)
        feasible_names = [v["vehicle_name"] for v in result["feasible"]]
        
        self.assertIn("ZEUS", feasible_names)
        # ECARS only has 350kg -> should be infeasible
        infeasible_names = [v["vehicle_name"] for v in result["infeasible"]]
        self.assertIn("ECARS 4x4", infeasible_names)


    def test_sensitivity_analysis(self):
        """
        Phase 7: Test sensitivity analysis output structure and evaluation.
        """
        req = {
            "Mission Role": "Surveillance",
            "Terrain": "Paved Road / Urban",
            "Payload": 50.0,
            "Operating Range": 10.0,
            "Minimum Mission Time": 0.5,
            "Maximum Mission Time": 2.0
        }
        prio = {k: "Medium" for k in req}
        weights = generate_weights(prio)
        
        result = rank_vehicles(VEHICLE_DATABASE, req, weights)
        self.assertIn("sensitivity", result)
        sens = result["sensitivity"]
        self.assertIn("is_stable", sens)
        self.assertIn("summary", sens)


if __name__ == "__main__":
    unittest.main()

