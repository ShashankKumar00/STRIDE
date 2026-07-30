from databases.vehicle_databases import vehicle_database

print("=" * 60)
print("STRIDE - Vehicle Database")
print("=" * 60)

for vehicle in vehicle_database:
    print(f"\nVehicle ID        : {vehicle['vehicle_id']}")
    print(f"Vehicle Name      : {vehicle['vehicle_name']}")
    print(f"Manufacturer      : {vehicle['manufacturer']}")
    print(f"Country           : {vehicle['country']}")
    print(f"Payload Capacity  : {vehicle['payload_capacity']} kg")
    print(f"Battery           : {vehicle['battery']}")
    print(f"Ground Clearance  : {vehicle['ground_clearance']} mm")
    print(f"Maximum Speed     : {vehicle['max_speed']} km/h")
    print(f"Terrain           : {', '.join(vehicle['terrain'])}")

    print("-" * 60)