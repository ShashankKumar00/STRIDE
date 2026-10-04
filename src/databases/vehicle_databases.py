# Vehicle Databases (Compatibility Wrapper for vehicle_database.py & vehicle_manager.py)
# Imports canonical dataset conforming to Phase 4 DATA_SCHEMA.md

from databases.vehicle_database import (
    VEHICLE_DATABASE,
    vehicle_database,
    display_all_vehicles
)
from databases.vehicle_manager import get_active_catalog, add_vehicle, load_custom_vehicles

# Dynamic active catalog by default
def get_all_vehicles():
    """Returns the combined catalog of base platforms + any custom added platforms."""
    return get_active_catalog()

__all__ = [
    "VEHICLE_DATABASE",
    "vehicle_database",
    "get_all_vehicles",
    "get_active_catalog",
    "add_vehicle",
    "load_custom_vehicles",
    "display_all_vehicles"
]