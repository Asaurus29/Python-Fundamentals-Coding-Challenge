from dataclasses import dataclass
from typing import List, Optional
import json
from pathlib import Path


# ======================= properties.py ================

@dataclass
class MaterialProperties:

    density: float
    yield_strength: float
    young_modulus: float
    # data properties holder vv important

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be greater than zero")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be greater than zero")
        if self.young_modulus <= 0:
            raise ValueError("Young's modulus must be greater than zero")

    def to_dict(self) -> dict:
        return {
            "density": self.density,
            "yield_strength": self.yield_strength,
            "young_modulus": self.young_modulus,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MaterialProperties":
        return cls(
            density=data["density"],
            yield_strength=data["yield_strength"],
            young_modulus=data["young_modulus"],
        )

# ======================= material.py =============

    """Base class for any material used in a stress test."""

    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    @property
    def name(self) -> str:
        return self._name
#no touch, causes infinite recursion destroy code

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
#store self._name

    @property
    def properties(self) -> MaterialProperties:
        return self._properties

    @properties.setter
    def properties(self, value: MaterialProperties) -> None:
        if not isinstance(value, MaterialProperties):
            raise ValueError("Properties must be a MaterialProperties instance")
        self._properties = value

    def hold_stress(self, stress: float) -> bool:
        """Return True if the material can withstand the given stress (MPa)."""
        return stress < self.properties.yield_strength

#controls what print(material) and str (material) shows

    def __str__(self) -> str:
        return f"{self.name} (Density: {self.properties.density} kg/m^3)"

 #check if two mats are = and if their name and properties match

    def __eq__(self, other) -> bool:
        if not isinstance(other, Material):
            return NotImplemented
        return self.name == other.name and self.properties == other.properties

 #define order by yield stregth it also fix sort and max
    def __lt__(self, other) -> bool:
        if not isinstance(other, Material):
            return NotImplemented
        return self.properties.yield_strength < other.properties.yield_strength

    def to_dict(self) -> dict:
        return {
            "type": type(self).__name__,
            "name": self.name,
            "properties": self.properties.to_dict(),
        }


class Metal(Material):
    def __init__(self, name: str, properties: MaterialProperties, is_ferrous: bool = False):
        super().__init__(name, properties) #reuse material
        self.is_ferrous = is_ferrous

#override material
    def __str__(self) -> str:
        ferrous_text = "Ferrous" if self.is_ferrous else "Not Ferrous"
        return f"{self.name} ({ferrous_text} metal, Density: {self.properties.density} kg/m^3)"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["is_ferrous"] = self.is_ferrous
        return data


class Plastic(Material):
    def __init__(self, name: str, properties: MaterialProperties, is_thermo: bool = True):
        super().__init__(name, properties)
        self.is_thermo = is_thermo

    def __str__(self) -> str:
        kind = "Thermoplastic" if self.is_thermo else "Not thermoplastic"
        return f"{self.name} ({kind} plastic, Density: {self.properties.density} kg/m^3)"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["is_thermo"] = self.is_thermo
        return data


class Composite(Material):
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        made_of_material: Material,
        strengthening_material: Material,
    ):
        super().__init__(name, properties)
        self.made_of_material = made_of_material
        self.strengthening_material = strengthening_material

    def __str__(self) -> str:
        return (
            f"{self.name} (Made of {self.made_of_material.name}, "
            f"Strengthened with {self.strengthening_material.name}, "
            f"Density: {self.properties.density} kg/m^3)"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["made_of_material"] = self.made_of_material.name
        data["strengthening_material"] = self.strengthening_material.name
        return data


# ======================= database.py =======================

DEFAULT_DATA_DIR = Path("data")
DEFAULT_MATERIALS_FILE = DEFAULT_DATA_DIR / "materials.json"


def get_material_database():
    # this is basically just a dictionary of all our starting materials
    # so we dont have to type all the numbers again every time we run the program
    materials = {
        "Steel": Metal(
            "Steel",
            MaterialProperties(density=7850, yield_strength=250, young_modulus=200),
            is_ferrous=True,
        ),
        "Aluminum": Metal(
            "Aluminum",
            MaterialProperties(density=2700, yield_strength=95, young_modulus=69),
            is_ferrous=False,
        ),
        "Titanium": Metal(
            "Titanium",
            MaterialProperties(density=4500, yield_strength=880, young_modulus=114),
            is_ferrous=False,
        ),
        "ABS Plastic": Plastic(
            "ABS Plastic",
            MaterialProperties(density=1040, yield_strength=40, young_modulus=2.3),
            is_thermo=True,
        ),
    }
    return materials


def add_composite_examples(materials_database):
    # adds one composite material made out of 2 of the materials above,
    # just so the Composite class actually gets used somewhere
    if "Steel" in materials_database and "ABS Plastic" in materials_database:
        steel = materials_database["Steel"]
        plastic = materials_database["ABS Plastic"]
        fiberglass_steel = Composite(
            "Fiberglass-Steel",
            MaterialProperties(density=1900, yield_strength=600, young_modulus=40),
            made_of_material=plastic,
            strengthening_material=steel,
        )
        materials_database["Fiberglass-Steel"] = fiberglass_steel


def save_materials_to_json(materials_database, filepath=DEFAULT_MATERIALS_FILE):
    # json.dump ,
    # itcant save file directly so calls dict
    # each one first to turn it into a plain dictionary
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)  # make the data folder if doesnt exist

    serializable = {}
    for name in materials_database:
        material = materials_database[name]
        serializable[name] = material.to_dict()

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)

    return filepath


def load_materials_from_json(filepath=DEFAULT_MATERIALS_FILE):
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"No materials database found at {filepath}")

    with filepath.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    materials = {}

    for name in raw:
        data = raw[name]
        if data["type"] == "Composite":
            continue
        materials[name] = material_from_dict(data)

    for name in raw:
        data = raw[name]
        if data["type"] != "Composite":
            continue
        props = MaterialProperties.from_dict(data["properties"])
        made_of_name = data["made_of_material"]
        strengthen_name = data["strengthening_material"]
        made_of = materials[made_of_name]
        strengthened_with = materials[strengthen_name]
        materials[name] = Composite(data["name"], props, made_of, strengthened_with)

    return materials


def material_from_dict(data):
    # checks if plastic metal or if in the data
    # makes json fiel
    props = MaterialProperties.from_dict(data["properties"])
    mat_type = data["type"]

    if mat_type == "Metal":
        return Metal(data["name"], props, is_ferrous=data.get("is_ferrous", False))
    elif mat_type == "Plastic":
        return Plastic(data["name"], props, is_thermo=data.get("is_thermo", True))
    elif mat_type == "Material":
        return Material(data["name"], props)
    else:
        raise ValueError(f"Unknown material type: {mat_type}")

#utils.py
def calculate_stress(force: float, area: float) -> float:
    """Calculates stress by dividing force by area."""
    if area <= 0:
        raise ValueError("Area must be greater than zero")
    return force / area

def calculate_strain(orig_len: float, ch_len: float) -> float:
  """Calculates strain by dividing change in length by original length."""
  if orig_len <= 0:
    raise ValueError("Original length must be greater than zero")
  return ch_len / orig_len

def calculate_factor_of_safety(yield_strength: float, stress: float) -> float:
  """Calculates the factor of safety by dividing yield strength by stress in MPa. """
  return yield_strength / (stress / 1_000_000)

def validate_positive(value: float, name: str) -> None:
  """Ensures the values are greater than zero."""
  if value <= 0:
    raise ValueError(f"{name} must be greater than zero")
  return value

def validate_non_negative(value: float, name: str) -> None:
  """Ensures the values are non-negative."""
  if value < 0:
    raise ValueError(f"{name} cannot be negative")
  return value

# ================== test.py ==============================
from typing import List, Optional
from material import Material


class StressTest:
    """Stress/strain measurement performed on a Material."""

    def __init__(
        self,
        material: Material,
        force: float,
        area: float,
        original_length: float,
        change_in_length: float,
        label: Optional[str] = None,
    ):
        if force <= 0:
            raise ValueError("Force must be positive")
        if area <= 0:
            raise ValueError("Area must be positive")
        if original_length <= 0:
            raise ValueError("Original length must be positive")
        if change_in_length < 0:
            raise ValueError("Change in length must be zero or positive")

        self.material = material
        self._force = force
        self._area = area
        self._original_length = original_length
        self._change_in_length = change_in_length
        self.label = label or f"{material.name} test"

    @property
    def stress(self) -> float:
        """Stress in MPa (force in N / area in m^2, scaled to MPa)."""
        return self._force / self._area

    @property
    def strain(self) -> float:
        return self._change_in_length / self._original_length


    @property
    def youngs_modulus(self) -> float:
        """Observed Young's modulus in GPa."""
        if self.strain == 0:
            return float("inf")
        return (self.stress / self.strain) / 1000

    @property
    def safety_factor(self) -> float:
        """Ratio of the material's yield strength to the applied stress."""
        return self.material.properties.yield_strength / self.stress

    def gonna_fail(self) -> bool:
        return self.stress >= self.material.properties.yield_strength

    def __str__(self) -> str:
        return (
            f"{self.label}: Stress = {self.stress:.2f} MPa, "
            f"Strain = {self.strain:.6f}, "
            f"E(observed) = {self.youngs_modulus:.2f} GPa, "
            f"Safety Factor = {self.safety_factor:.2f}"
        )

    def __lt__(self, other) -> bool:
        if not isinstance(other, StressTest):
            return NotImplemented
        return self.stress < other.stress


class TestAnalysis:
    """Collects StressTest results and reports on them (a session's history)."""

    def __init__(self, name: str = "Materials Test"):
        self.name = name
        self._tests: List[StressTest] = []

    @property
    def tests(self) -> List[StressTest]:
        return list(self._tests)


    def add_test(self, test: StressTest):
        if not isinstance(test, StressTest):
            raise ValueError("Test must be of type StressTest")
        self._tests.append(test)
        print("Calculation added to history.")

    def test_material(self, material_name: str) -> List[StressTest]:


    def strongest_material(self) -> Optional[Material]:
        materials = {t.material.name: t.material for t in self._tests}
        if not materials:
            return None
        return max(materials.values(), key=lambda mat: mat.properties.yield_strength)


    def highest_stress_test(self) -> Optional[StressTest]:
        if not self._tests:
            return None
        return max(self._tests, key=lambda test: test.stress)


    def failed_tests(self) -> List[StressTest]:
        return [t for t in self._tests if t.gonna_fail()]


    def average_youngs_modulus(self, material_name: str) -> Optional[float]:
        relevant = self.test_material(material_name)
        if not relevant:
            return None
        return sum(t.youngs_modulus for t in relevant) / len(relevant)

    def summary(self) -> str:
        if not self.tests:
            return f"{self.name}: no tests recorded yet."


        lines = [f"-- {self.name}: Summary report --", f"Total Tests: {len(self.tests)}"]
        materials = sorted({t.material.name for t in self.tests})

        for material_name in materials:
            mat_tests = self.test_material(material_name)
            avg_e = self.average_youngs_modulus(material_name)
            fails = [t for t in mat_tests if t.gonna_fail()]
            lines.append(
                f"- {material_name}: {len(mat_tests)} test(s), "
                f"avg E={avg_e:.2f} GPa, failures={len(fails)}"
            )

        strongest = self.strongest_material()
        if strongest:
            lines.append(f"Strongest material: {strongest.name}")

        hardest = self.highest_stress_test()
        if hardest:
            lines.append(f"Highest-stress test: {hardest}")

        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._tests)

    def __str__(self) -> str:
        return f"{self.name} ({len(self._tests)} test(s) recorded)"

#main.py
def get_float_input(prompt: str) -> float:
    """Keep asking the user until a valid number is entered."""
    while True:
        raw = input(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def choose_material(materials: dict):
    """pick stuff from dict"""
    names = list(materials.keys())
    if not names:
        print("No materials available.")
        return None

    print("\nAvailable materials:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")

    while True:
        choice = input(f"Choose a material (1-{len(names)}): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(names):
                return materials[names[index]]
        except ValueError:
            pass
        print("Invalid choice, please try again.")


def list_materials(materials: dict) -> None:
    """Print every material currently in the database."""
    if not materials:
        print("No materials in the database.")
        return
    print("\n--- Material Database ---")
    for material in materials.values():
        print(material)


def run_stress_test(materials: dict, analysis: TestAnalysis) -> None:
    """Prompt the user for test inputs, build a StressTest, and record it."""
    material = choose_material(materials)
    if material is None:
        return

    force = get_float_input("Applied force (N): ")
    area = get_float_input("Cross-sectional area (m^2): ")
    orig_len = get_float_input("Original length (m): ")
    ch_len = get_float_input("Change in length (m): ")
    label = input("Label for this test (optional, press Enter to skip): ").strip() or None

#stress test and adds value thingy
    try:
        test = StressTest(
            material=material,
            force=force,
            area=area,
            original_length=orig_len,
            change_in_length=ch_len,
            label=label,
        )
    except ValueError as e:
        print(f"Input error: {e}")
        return

    analysis.add_test(test)
    print(f"\n--- Results ---\n{test}")


#add def main
def main() -> None:
    """Main program loop: shows the menu and routes user choices."""
    materials = get_material_database()
    add_composite_examples(materials)
    analysis = TestAnalysis("Stress and Strain Test Session")

    while True:
        print("\n=== Stress and Strain Analysis System ===")
        print("1. Run a stress/strain test on a material")
        print("2. List available materials")
        print("3. View session summary")
        print("4. Save materials database to JSON")
        print("5. Load materials database from JSON")
        print("6. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            run_stress_test(materials, analysis)
        elif choice == "2":
            list_materials(materials)
        elif choice == "3":
            print(f"\n{analysis.summary()}")
        elif choice == "4":
            path = save_materials_to_json(materials)
            print(f"Materials saved to {path}")
        elif choice == "5":
            try:
                materials = load_materials_from_json()
                print("Materials loaded successfully.")
            except FileNotFoundError as e:
                print(e)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-6.")

if _name_ == "_main_":
    main()
