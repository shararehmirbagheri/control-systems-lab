# Data Center Power Estimator

print("=== QTS Data Center Power Estimator ===")

num_racks = int(input("Number of racks: "))
avg_kw_per_rack = float(input("Average kW per rack: "))
pue = float(input("PUE (example 1.3): "))

it_load = num_racks * avg_kw_per_rack
facility_load = it_load * pue

annual_kwh = facility_load * 24 * 365

print("\n===== Results =====")
print(f"IT Load: {it_load:.2f} kW")
print(f"Facility Load: {facility_load:.2f} kW")
print(f"Annual Energy: {annual_kwh:,.0f} kWh")

if facility_load > 1000:
    print("Classification: Megawatt-scale deployment")
else:
    print("Classification: Small/Medium deployment")

