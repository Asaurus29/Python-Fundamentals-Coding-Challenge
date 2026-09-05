def create_calculation_method(material: str, inputs: dict, results: dict) -> dict:
  """ Create a calculation method.

  Inputs:
  material (str): The material used in the calculation.
  inputs (dict): A dictionary of the inputs to the calculation.
  results (dict): A dictionary of the results of the calculation.

  Returns:
  calculation_method (dict): A dictionary containing the material, inputs, and results.
  """
  calculation_method = {
    "material": material,
    "inputs": inputs,
    "results": results
  }
  return calculation_method

def add_to_history(calculation_method: dict, history: list) -> None:
  """ Add a calculation method to the history. """
  history.append(calculation_method)
  print("Calculation added to history.")

def get_material_database() -> dict:
  """ Return a dictionary of material properties. """
  materials = {
      "Steel": {"yield_strength": 250, "youngs_modulus": 200},
      "Aluminum": {"yield_strength": 95, "youngs_modulus": 69},
      "Titanium": {"yield_strength": 880, "youngs_modulus": 114}
  }
  return materials

def get_material_properties(material: str, materials_database: dict) -> dict:
  """ Return a dictionary of material properties. """
  if material not in materials_database:
    raise ValueError(f"Material '{material}' not found in the database.")
  return materials_database[material]

#Input Validation
def validate_input(force: float, area: float, orig_len: float, ch_len: float) -> None:
  """ Validate that all input values are valid.

  Inputs:
  force (float): The applied force in newtons.
  area (float): The cross-sectional area in square meters.
  orig_len (float): The original length of the material in meters.
  ch_len (float): The change in length in meters.

  Returns:
  None

  Raises:
  ValueError: If any of the input values are invalid.
  """
  if force <= 0:
    raise ValueError("Force must be greater than 0")
  if area <= 0:
    raise ValueError("Area must be greater than 0")
  if orig_len <= 0:
    raise ValueError("Original length must be greater than 0")
  if ch_len < 0:
    raise ValueError("Change in length must be greater than 0")

#Core Calculation
def calculate_stress(force: float, area: float) -> float:
  """ Calculate the stress.

  Inputs:
  force (float): The applied force in newtons.
  area (float): The cross-sectional area in square meters.

  Returns:
  stress (float): The stress in newtons per square meter.
  """
  stress = force / area
  return stress

def calculate_strain(orig_len: float, ch_len: float) -> float:
  """ Calculate the strain.

  Inputs:
  orig_len (float): The original length of the material in meters.
  ch_len (float): The change in length in meters.

  Returns:
  strain (float): The strain.
  """
  strain = ch_len / orig_len
  return strain

def calculate_youngs_modulus(stress: float, strain: float) -> float:
  """ Calculate the Young's modulus.

  Inputs:
  stress (float): The stress in newtons per square meter.
  strain (float): The strain.

  Returns:
  youngs_modulus (float): The Young's modulus in Pascals.

  Raises:
  ValueError: If the stress or strain is zero.
  """
  if stress == 0:
    raise ValueError("Error. Stress cannot be zero.")
  if strain == 0:
    raise ValueError("Error. Strain cannot be zero.")
  youngs_modulus = stress / strain
  return youngs_modulus

def calculate_factor_of_safety(yield_strength: float, stress: float) -> float:
  """ Calculate the factor of safety.

  Inputs:
  yield_strength (float): The yield strength in Pascals.
  stress (float): The stress in newtons per square meter.

  Returns:
  safety_factor (float): The factor of safety.
  """
  safety_factor = yield_strength / (stress / 1_000_000)
  return safety_factor

#Display and output
def display_material_menu(materials_database: dict) -> None:
  """ Display the material menu. """
  print("Material Menu:")
  for material in materials_database:
    print(f"  - {material}")

def display_calculation_results(results: dict) -> None:
  """ Display the calculation results. """
  print("Calculation Results:")
  print(f"Stress: {results['stress']/1_000_000:.2f} MPa")
  print(f"Strain: {results['strain']:.6f}")
  print(f"Young's Modulus: {results['youngs_modulus']} GPa")
  print(f"Yield Strength: {results['yield_strength']} MPa")
  print(f"Safety Factor: {results['safety_factor']:.2f}")

def display_session_summary(history: list) -> None:
  """ Display the session summary. """
  print("Session Summary:")
  if not history:
    print("No calculations performed yet.")
    return
  for i, calculation_method in enumerate(history):
    print(f"\n--- Calculation {i+1} ---")
    print(f"Material: {calculation_method['material']}")
    print("Inputs:")
    for key, value in calculation_method["inputs"].items():
      print(f"{key.replace('_', ' ').title()}: {value:.2e}")
    print("Results:")
    print(f"Stress: {calculation_method['results']['stress']/1_000_000:.2f} MPa")
    print(f"Strain: {calculation_method['results']['strain']:.6f}")
    print(f"Young's Modulus: {calculation_method['results']['youngs_modulus']} GPa")
    print(f"Yield Strength: {calculation_method['results']['yield_strength']} MPa")
    print(f"Safety Factor: {calculation_method['results']['safety_factor']:.2f}")

def display_safety_analysis(stress: float, yield_strength: float, safety_factor: float) -> None:
  """ Display the safety analysis. """
  stress_mpa = stress / 1_000_000
  print("Safety Analysis:")
  print(f"Stress: {stress_mpa:.2f} MPa")
  print(f"Yield Strength: {yield_strength:.2e} MPa")
  print(f"Safety Factor: {safety_factor:.2f}")
  if safety_factor >= 2:
    print("Safe.")
  elif safety_factor >= 1:
    print("Warning. Not safe.")
  else:
    print("Unsafe.")

#Main
def main() -> None:
  """ Main function to orchestrate all the calculations """
  materials_database = get_material_database()
  history = []

  while True:
    print("-"*60)
    print("Welcome to the Stress and Strain Calculator!".center(60))
    print("-"*60)
    print()

    display_material_menu(materials_database)
    print("  - Custom")
    material = input("Enter the material (or type 'exit' to quit): ")
    if material.lower() == "exit":
      break

    try:
      if material.lower() == "custom":
        material = input("Enter the material name: ")
        yield_strength = float(input("Enter the yield strength (in MPa): "))
        youngs_modulus = float(input("Enter the Young's modulus (in GPa): "))
        material_properties = {"yield_strength": yield_strength, "youngs_modulus": youngs_modulus}
        materials_database[material] = material_properties
        material = material
      else:
        material_properties = get_material_properties(material, materials_database)

      force = float(input("Enter the applied force (in newtons): "))
      area = float(input("Enter the cross-sectional area (in square meters): "))
      orig_len = float(input("Enter the original length of the material (in meters): "))
      ch_len = float(input("Enter the change in length (in meters): "))
      validate_input(force, area, orig_len, ch_len)

      stress = calculate_stress(force, area)
      strain = calculate_strain(orig_len, ch_len)

      youngs_modulus = calculate_youngs_modulus(stress, strain) / 1_000_000_000

      safety_factor = calculate_factor_of_safety(material_properties["yield_strength"], stress)

      inputs = {
        "force": force,
        "area": area,
        "orig_len": orig_len,
        "ch_len": ch_len
      }

      results = {
        "stress": stress,
        "strain": strain,
        "youngs_modulus": material_properties["youngs_modulus"],
        "yield_strength": material_properties["yield_strength"],
        "safety_factor": safety_factor
      }

      calculation_method = create_calculation_method(material, inputs, results)
      add_to_history(calculation_method, history)

      display_calculation_results(results)
      display_safety_analysis(stress, material_properties["yield_strength"], safety_factor)

    except ValueError as e:
      print(f"Error: {e}")
      continue

  display_session_summary(history)
  print("Closing program...")

if __name__ == "__main__":
  main()
