# Vehicle Databases (Compatibility Wrapper for vehicle_database.py)
# Imports canonical dataset conforming to Phase 4 DATA_SCHEMA.md

from databases.vehicle_database import (
    VEHICLE_DATABASE,
    vehicle_database,
    get_all_vehicles,
    display_all_vehicles
)

__all__ = ["VEHICLE_DATABASE", "vehicle_database", "get_all_vehicles", "display_all_vehicles"]