# Stress and Strain Calculator
print("Stress and Strain Calculator".center(60))

MEASUREMENT_UNITS = ("Newtons (N)", "Square Meters (m²)", "Meters (m)", "Pascals (Pa)", "Megapascals (MPa)", "Gigapascals (GPa)")

calculation_history = []

unique_materials = set()

materials = {
    "1": {"name": "Steel", "yield_strength": 250, "youngs_modulus": 200},
    "2": {"name": "Aluminum", "yield_strength": 95, "youngs_modulus": 69},
    "3": {"name": "Titanium", "yield_strength": 880, "youngs_modulus": 114}
}

while True:
    print()
    print("-" * 60)
    print()

    print("Select a Material:")
    print("1. Steel")
    print("2. Aluminum")
    print("3. Titanium")
    print("4. Custom Material")

    while True:
        choice = input("Enter your choice (1 / 2 / 3 / 4): ")

        if choice in materials:
            material = materials[choice]
            break

        elif choice == "4":
            custom = input("Enter your custom material name: ")

            while True:
                try:
                    yield_strength = float(
                        input(f"Enter the yield strength in {MEASUREMENT_UNITS[4]}: ")
                    )

                    if yield_strength > 0:
                        break
                    else:
                        print("Error: Yield strength must be greater than 0.")

                except ValueError:
                    print("Error: Please enter a valid number.")

            while True:
                try:
                    youngs_modulus = float(
                        input(f"Enter the Young's modulus in {MEASUREMENT_UNITS[5]}: ")
                    )

                    if youngs_modulus > 0:
                        break
                    else:
                        print("Error: Young's modulus must be greater than 0.")

                except ValueError:
                    print("Error: Please enter a valid number.")

            material = {
                "name": custom,
                "yield_strength": yield_strength,
                "youngs_modulus": youngs_modulus
            }

            break

        else:
            print("Error: Please choose among the available materials.")

    print()
    print(f"Selected Material: {material['name']}")
    print(f"Yield Strength: {material['yield_strength']} {MEASUREMENT_UNITS[4]}")
    print(f"Young's Modulus: {material['youngs_modulus']} {MEASUREMENT_UNITS[5]}")

    while True:
        try:
            force = float(input(f"Enter the applied force in {MEASUREMENT_UNITS[0]}: "))
            area = float(input(f"Enter the area in {MEASUREMENT_UNITS[1]}: "))
            orig_len = float(input(f"Enter the original length of the material in {MEASUREMENT_UNITS[2]}: "))
            ch_len = float(input(f"Enter the change in length in {MEASUREMENT_UNITS[2]}: "))

            if force < 0:
                print("Error: Force cannot be negative.")
                continue
            elif area <= 0:
                print("Error: Area must be greater than 0.")
                continue
            elif orig_len <= 0:
                print("Error: Original length must be greater than 0.")
                continue
            elif ch_len < 0:
                print("Error: Change in length cannot be negative.")
                continue
            else:
                stress = force / area
                strain = ch_len / orig_len

                stress_mpa = stress / 1_000_000

                print()
                print(f"Stress = {stress} {MEASUREMENT_UNITS[3]}")
                print(f"Stress = {stress_mpa:.2f} {MEASUREMENT_UNITS[4]}")
                print(f"Strain = {strain:.6f}")

                factor_of_safety = material["yield_strength"] / stress_mpa

                if factor_of_safety >= 2:
                    safety_status = "SAFE"
                    print(f"SAFE - Factor of safety: {factor_of_safety:.0f}")
                elif factor_of_safety >= 1:
                    safety_status = "CAUTION"
                    print(f"CAUTION - Factor of safety: {factor_of_safety:.2f}")
                else:
                    safety_status = "UNSAFE"
                    print(f"UNSAFE - Factor of safety: {factor_of_safety:.2f}")

                if stress_mpa >= material["yield_strength"]:
                    print("Warning: The material has reached or exceeded its yield strength.")
                else:
                    print("The material is below its yield strength.")

                test_info = {
                    "material": material["name"],
                    "force": force,
                    "area": area,
                    "original_length": orig_len,
                    "change_in_length": ch_len,
                    "stress": stress_mpa,
                    "strain": strain,
                    "youngs_modulus": material["youngs_modulus"],
                    "safety_result": safety_status
                }

                calculation_history.append(test_info)

                unique_materials.add(material["name"])

        except ValueError:
            print("Error: Please enter valid characters (numbers only).")
            continue

        break

    while True:
        again = input("\nContinue calculation? (y/n): ")

        if again.lower() == "y":
            break
        elif again.lower() == "n":
            print("\nClosing program and generating summary...")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    if again.lower() == "n":
        break

print("\n" + "=" * 60)
print("SESSION SUMMARY".center(60))
print("=" * 60)

total_tests = len(calculation_history)
print(f"Total Calculations Performed: {total_tests}")

if total_tests > 0:
    print(f"Unique Materials Tested: {', '.join(unique_materials)}")

    stresses = [test["stress"] for test in calculation_history]
    strains = [test["strain"] for test in calculation_history]

    max_stress = max(stresses)
    min_stress = min(stresses)
    avg_stress = sum(stresses) / total_tests
    max_strain = max(strains)

    print("\n--- Statistical Overview ---")
    print(f"Highest Stress Recorded: {max_stress:.2f} {MEASUREMENT_UNITS[4]}")
    print(f"Lowest Stress Recorded: {min_stress:.2f} {MEASUREMENT_UNITS[4]}")
    print(f"Average Stress: {avg_stress:.2f} {MEASUREMENT_UNITS[4]}")
    print(f"Highest Strain Recorded: {max_strain:.6f}")

    safe_count = sum(1 for test in calculation_history if test["safety_result"] == "SAFE")
    caution_count = sum(1 for test in calculation_history if test["safety_result"] == "CAUTION")
    unsafe_count = sum(1 for test in calculation_history if test["safety_result"] == "UNSAFE")

    print("\n--- Safety Breakdown ---")
    print(f"SAFE tests: {safe_count}")
    print(f"CAUTION tests: {caution_count}")
    print(f"UNSAFE tests: {unsafe_count}")

print("=" * 60)