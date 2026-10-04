import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from planning.route_planner import calculate_route_feasibility, simulate_grid_route


class TestRoutePlanning(unittest.TestCase):

    def setUp(self):
        self.fast_long_range_ugv = {
            "vehicle_name": "Vrishabh",
            "mobility_type": "Wheeled 4x4",
            "max_speed_kmh": 50.0,
            "operating_range_km": 100.0
        }
        self.short_range_ugv = {
            "vehicle_name": "ShortRangeUGV",
            "mobility_type": "Wheeled 4x4",
            "max_speed_kmh": 20.0,
            "operating_range_km": 12.0
        }

    def test_route_feasibility_pass(self):
        """Test feasible vehicle under nominal conditions."""
        res = calculate_route_feasibility(
            self.fast_long_range_ugv,
            terrain_name="Plain / Grassland",
            nominal_distance_km=20.0,
            max_time_hours=2.0
        )
        self.assertTrue(res["is_route_feasible"])
        self.assertGreater(res["effective_distance_km"], 20.0)
        self.assertLess(res["transit_duration_hours"], 2.0)

    def test_detour_expansion_disqualifies_marginal_range(self):
        """
        Paper 5 Finding: A vehicle whose nominal range appears sufficient for
        straight-line distance (12 km range >= 10 km nominal) is disqualified
        once the terrain detour factor expands route distance to 13.5 km.
        """
        res = calculate_route_feasibility(
            self.short_range_ugv,
            terrain_name="Mud / Soft Ground",  # Detour factor 1.35 -> 13.5 km
            nominal_distance_km=10.0,
            max_time_hours=3.0
        )
        # Should fail because 12.0 km range < 13.5 km effective route distance!
        self.assertFalse(res["is_route_feasible"])
        self.assertTrue(any("insufficient for detour-adjusted route" in r for r in res["failure_reasons"]))

    def test_a_star_grid_path_found(self):
        """Test that A* successfully finds a path on the 20x20 terrain grid."""
        sim = simulate_grid_route(
            self.fast_long_range_ugv,
            terrain_name="Plain / Grassland",
            grid_size=(20, 20),
            seed=42
        )
        self.assertTrue(sim["success"])
        self.assertGreater(sim["total_steps"], 20)
        self.assertEqual(sim["path_waypoints"][0], (0, 0))
        self.assertEqual(sim["path_waypoints"][-1], (19, 19))

    def test_a_star_cost_reflects_terrain_difficulty(self):
        """A* total path cost in mud should be higher than on paved road."""
        sim_paved = simulate_grid_route(
            self.fast_long_range_ugv,
            terrain_name="Paved Road / Urban",
            grid_size=(15, 15),
            seed=100
        )
        sim_mud = simulate_grid_route(
            self.fast_long_range_ugv,
            terrain_name="Mud / Soft Ground",
            grid_size=(15, 15),
            seed=100
        )
        self.assertTrue(sim_paved["success"])
        self.assertTrue(sim_mud["success"])
        self.assertGreater(sim_mud["total_cost"], sim_paved["total_cost"])


if __name__ == "__main__":
    unittest.main()
