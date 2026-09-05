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

