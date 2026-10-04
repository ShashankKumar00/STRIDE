import unittest
import os
import sys

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from databases.vehicle_manager import add_vehicle, get_active_catalog, reset_custom_vehicles, validate_vehicle_input
from mission.mission_parser import parse_mission_narrative
from databases.scoring_engine import rank_vehicles
from databases.priority_weights import generate_weights


class TestVehicleManagerAndParser(unittest.TestCase):

    def setUp(self):
        reset_custom_vehicles()

    def tearDown(self):
        reset_custom_vehicles()

    # 1. Platform Ingestion & Custom Vehicle Manager Tests
    def test_add_valid_custom_platform(self):
        """Test: Valid custom OEM platform is successfully ingested and assigned unique ID."""
        new_platform = {
            "vehicle_name": "Bharat Sentinel 4x4",
            "manufacturer": "Bharat Forge Defence",
            "mobility_type": "Wheeled 4x4",
            "mission_roles": ["Surveillance", "Combat / Tactical Support"],
            "terrain_capabilities": ["Paved Road / Urban", "Plain / Grassland", "Desert / Sand"],
            "payload_capacity_kg": "300.0",
            "max_speed_kmh": "28.0",
            "operating_range_km": "40.0",
            "endurance_hours": "8.0",
            "max_control_range_km": "15.0",
            "status": "Field Trials / Evaluated"
        }
        success, msg, v = add_vehicle(new_platform)
        self.assertTrue(success, f"Failed to add valid vehicle: {msg}")
        self.assertTrue(v["vehicle_id"].startswith("UGV-OEM-"))
        
        catalog = get_active_catalog()
        self.assertEqual(len(catalog), 25)
        names = [item["vehicle_name"] for item in catalog]
        self.assertIn("Bharat Sentinel 4x4", names)

    def test_duplicate_name_rejected(self):
        """Test: Adding a vehicle with an existing name is rejected."""
        existing_vehicle = {
            "vehicle_name": "MUNTRA-S",  # Already in base database
            "manufacturer": "Another Corp",
            "mobility_type": "Tracked",
            "mission_roles": ["Surveillance"],
            "terrain_capabilities": ["Desert / Sand"]
        }
        success, msg, _ = add_vehicle(existing_vehicle)
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_missing_mandatory_fields_rejected(self):
        """Test: Ingesting a platform without mandatory name or roles fails validation."""
        is_valid, msg = validate_vehicle_input({"vehicle_name": ""})
        self.assertFalse(is_valid)

        is_valid2, msg2 = validate_vehicle_input({
            "vehicle_name": "ValidName",
            "manufacturer": "ValidManuf",
            "mobility_type": "Tracked",
            "mission_roles": []  # Empty roles
        })
        self.assertFalse(is_valid2)

    # 2. Smart Mission Narrative Parser Tests
    def test_parse_ladakh_high_altitude_mission(self):
        """Test: Parser extracts high-altitude, reconnaissance, and cold weather parameters."""
        narrative = "Need high altitude reconnaissance patrol in Ladakh at 15000 ft in sub-zero snow terrain, carrying 50 kg sensor payload with silent electric stealth and 10 km standoff"
        res = parse_mission_narrative(narrative)
        self.assertIn("Reconnaissance", res["roles"])
        self.assertEqual(res["terrain"], "Snow / Ice")
        self.assertEqual(res["payload_kg"], 50.0)
        self.assertEqual(res["altitude_m"], 4572)  # 15000 ft * 0.3048
        self.assertEqual(res["temperature_c"], -20.0)
        self.assertTrue(res["stealth_required"])

    def test_parse_desert_heavy_logistics_mission(self):
        """Test: Parser extracts desert terrain, heavy payload, and time window."""
        narrative = "Execute heavy logistics resupply mission across Thar desert sand dunes carrying 500 kg ammunition over 15 km within 3 hours"
        res = parse_mission_narrative(narrative)
        self.assertIn("Logistics / Transport / Casualty Evacuation", res["roles"])
        self.assertEqual(res["terrain"], "Desert / Sand")
        self.assertEqual(res["payload_kg"], 500.0)
        self.assertEqual(res["operating_range_km"], 15.0)
        self.assertEqual(res["max_time_hours"], 3.0)

    # 3. Tactical Parameters in Decision Engine
    def test_tactical_standoff_constraint(self):
        """Test: Standoff distance hard constraint disqualifies platforms with insufficient control link range."""
        catalog = get_active_catalog()
        req = {
            "Mission Role": "Surveillance",
            "Terrain": "Paved Road / Urban",
            "Payload": 10.0,
            "Operating Range": 5.0,
            "Minimum Mission Time": 0.5,
            "Maximum Mission Time": 2.0,
            "Standoff Distance": 12.0  # Requires at least 12 km control standoff
        }
        weights = generate_weights({k: "Medium" for k in req})
        results = rank_vehicles(catalog, req, weights)
        feasible = results.get("feasible", [])
        
        # All feasible vehicles must have control range >= 12.0 km
        for v in feasible:
            ctrl_range = v["details"].get("max_control_range_km", 0.0) or 0.0
            self.assertGreaterEqual(ctrl_range, 12.0)

    def test_tactical_altitude_constraint(self):
        """Test: High altitude ceiling constraint filters platforms uncertified for extreme elevation."""
        catalog = get_active_catalog()
        req = {
            "Mission Role": "Surveillance",
            "Terrain": "Rugged / Mountainous / Rocky",
            "Payload": 10.0,
            "Operating Range": 5.0,
            "Minimum Mission Time": 0.5,
            "Maximum Mission Time": 2.0,
            "Operational Altitude": 5000  # 5,000 m ASL (Himalayan passes)
        }
        weights = generate_weights({k: "Medium" for k in req})
        results = rank_vehicles(catalog, req, weights)
        feasible = results.get("feasible", [])

        # Platforms like BEML High-Alt UGV (5500m) or Torus MARS (5200m) or TASL (5000m) should be qualified
        feasible_names = [v["vehicle_name"] for v in feasible]
        self.assertTrue(any("BEML" in n or "Torus" in n or "TASL" in n for n in feasible_names))

        # Check disqualified reasons for platforms rated only for lower altitudes
        infeasible = results.get("infeasible", [])
        for inf in infeasible:
            reasons = inf.get("explanation", {}).get("failed_constraints", [])
            # If failed on altitude, reason must be clear
            for r in reasons:
                if "altitude ceiling" in r:
                    self.assertIn("m ASL", r)


if __name__ == "__main__":
    unittest.main()
