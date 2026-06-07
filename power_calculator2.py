# Power Calculator
print("Three-Phase Power Calculator")

voltage = float(input("Enter Voltage (V): "))
current = float(input("Enter Current (A): "))

power_kw = voltage * current * 1.732 / 1000

print(f"\nPower = {power_kw:.2f} kW")