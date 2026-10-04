import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from terrain.terrain_model import STANDARD_TERRAINS, get_terrain_profile
from terrain.traversability import calculate_traversability


class TestTerrainPrototype(unittest.TestCase):

    def setUp(self):
        self.tracked_ugv = {
            "vehicle_name": "MUNTRA-S",
            "mobility_type": "Tracked",
            "max_speed_kmh": 20.0
        }
        self.wheeled_4x4_ugv = {
            "vehicle_name": "Vrishabh",
            "mobility_type": "Wheeled 4x4",
            "max_speed_kmh": 50.0
        }
        self.wheeled_6x6_ugv = {
            "vehicle_name": "BRUTE",
            "mobility_type": "Wheeled 6x6",
            "max_speed_kmh": 10.0
        }

    def test_terrain_profile_retrieval(self):
        """Test retrieving standard terrain profiles."""
        paved = get_terrain_profile("Paved Road / Urban")
        self.assertEqual(paved.friction_coefficient, 0.85)
        self.assertEqual(paved.detour_factor, 1.05)
        
        mud = get_terrain_profile("Mud / Soft Ground")
        self.assertEqual(mud.detour_factor, 1.35)

    def test_tracked_vs_wheeled_in_mud(self):
        """
        Paper 4 Hypothesis: Tracked vehicles have superior floatation in mud
        compared to Wheeled 4x4.
        """
        tracked_mud = calculate_traversability(self.tracked_ugv, "Mud / Soft Ground")
        wheeled_mud = calculate_traversability(self.wheeled_4x4_ugv, "Mud / Soft Ground")
        
        # Tracked traversability should be significantly higher in mud
        self.assertGreater(tracked_mud["traversability_index"], wheeled_mud["traversability_index"])
        self.assertLess(tracked_mud["terrain_cost"], wheeled_mud["terrain_cost"])

    def test_wheeled_superior_speed_on_road(self):
        """
        Wheeled vehicles achieve higher effective speeds on paved roads.
        """
        tracked_road = calculate_traversability(self.tracked_ugv, "Paved Road / Urban")
        wheeled_road = calculate_traversability(self.wheeled_4x4_ugv, "Paved Road / Urban")
        
        self.assertGreater(wheeled_road["effective_speed_kmh"], tracked_road["effective_speed_kmh"])

    def test_extreme_slope_infeasible(self):
        """
        Exceeding vehicle climbing limit should derate traversability to near zero.
        """
        steep_result = calculate_traversability(self.wheeled_4x4_ugv, "Rugged / Mountainous / Rocky", slope_deg=35.0)
        # Max slope for 4x4 is 22 deg, 35 deg should cause severe drop in traversability
        self.assertLess(steep_result["traversability_index"], 0.15)


if __name__ == "__main__":
    unittest.main()
