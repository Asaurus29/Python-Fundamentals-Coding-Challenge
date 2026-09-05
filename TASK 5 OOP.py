

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MaterialProperties:
    """Physical properties of a material.

    density (kg/m^3), yield_strength (MPa), young_modulus (GPa)
    """
    density: float
    yield_strength: float
    young_modulus: float
#data properties holder vv important

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be greater than zero")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be greater than zero")
        if self.young_modulus <= 0:
            raise ValueError("Young's modulus must be greater than zero")


class Material:
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


class Metal(Material):
    def __init__(self, name: str, properties: MaterialProperties, is_ferrous: bool = False):
        super().__init__(name, properties) #reuse material
        self.is_ferrous = is_ferrous

#override material
    def __str__(self) -> str:
        ferrous_text = "Ferrous" if self.is_ferrous else "Not Ferrous"
        return f"{self.name} ({ferrous_text} metal, Density: {self.properties.density} kg/m^3)"


class Plastic(Material):
    def __init__(self, name: str, properties: MaterialProperties, is_thermo: bool = True):
        super().__init__(name, properties)
        self.is_thermo = is_thermo

    def __str__(self) -> str:
        kind = "Thermoplastic" if self.is_thermo else "Not thermoplastic"
        return f"{self.name} ({kind} plastic, Density: {self.properties.density} kg/m^3)"


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


class StressTest:
    """A single stress/strain measurement performed on a Material."""

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
        #stored with undescore
        #do not reassign
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
#orgi length

    @property
    def youngs_modulus(self) -> float:
        """Observed Young's modulus in GPa."""
        if self.strain == 0:
            #to avoid zerodivisionerror
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
#returns a copy of list so callers cant mess the internal

    def add_test(self, test: StressTest):
        if not isinstance(test, StressTest):
            raise ValueError("Test must be of type StressTest")
        self._tests.append(test)
        print("Calculation added to history.")

    def test_material(self, material_name: str) -> List[StressTest]:
        return [t for t in self.tests if t.material.name == material_name]
#test for material somehow its working

    def strongest_material(self) -> Optional[Material]:
        materials = {t.material.name: t.material for t in self._tests}
        if not materials:
            return None
        return max(materials.values(), key=lambda mat: mat.properties.yield_strength)
      #don't touch I don't know how it works but its working

    def highest_stress_test(self) -> Optional[StressTest]:
        if not self._tests:
            return None
        return max(self._tests, key=lambda test: test.stress)
#single test reach high value

    def failed_tests(self) -> List[StressTest]:
        return [t for t in self._tests if t.gonna_fail()]
# the low value

    def average_youngs_modulus(self, material_name: str) -> Optional[float]:
        relevant = self.test_material(material_name)
        if not relevant:
            return None
        return sum(t.youngs_modulus for t in relevant) / len(relevant)

    def summary(self) -> str:
        if not self.tests:
            return f"{self.name}: no tests recorded yet."

#build the multi line
        lines = [f"-- {self.name}: Summary report --", f"Total Tests: {len(self.tests)}"]
        materials = sorted({t.material.name for t in self.tests})
   # gives value on the material
        for material_name in materials:
            mat_tests = self.test_material(material_name)
            avg_e = self.average_youngs_modulus(material_name)
            fails = [t for t in mat_tests if t.gonna_fail()]
            lines.append(
                f"- {material_name}: {len(mat_tests)} test(s), "
                f"avg E={avg_e:.2f} GPa, failures={len(fails)}"
            )
#adds the strongest and hardest
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


def get_material_database() -> Dict[str, Material]:
    """Return the built-in materials, keyed by name."""
    return {
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
    }


def display_material_menu(materials_database: Dict[str, Material]) -> None:
    print("Material Menu:")
    for name in materials_database:
        print(f"  - {name}")
    print("  - Custom")


def display_test_results(test: StressTest) -> None:
    print("Calculation Results:")
    print(f"Stress: {test.stress:.2f} MPa")
    print(f"Strain: {test.strain:.6f}")
    print(f"Young's Modulus (observed): {test.youngs_modulus:.2f} GPa")
    print(f"Yield Strength: {test.material.properties.yield_strength} MPa")
    print(f"Safety Factor: {test.safety_factor:.2f}")


def display_safety_analysis(test: StressTest) -> None:
    print("Safety Analysis:")
    print(f"Stress: {test.stress:.2f} MPa")
    print(f"Yield Strength: {test.material.properties.yield_strength:.2f} MPa")
    print(f"Safety Factor: {test.safety_factor:.2f}")
    if test.safety_factor >= 2:
        print("Safe.")
    elif test.safety_factor >= 1:
        print("Warning. Marginal - close to failure.")
    else:
        print("Unsafe. Material will yield.")


def display_session_summary(analysis: TestAnalysis) -> None:
    print(analysis.summary())


def main() -> None:
    """Interactive loop: pick a material, enter test conditions, see results."""
    materials_database = get_material_database()
    analysis = TestAnalysis("Interactive Session")

    while True:
        print("-" * 60)
        print("Welcome to the Stress and Strain Calculator!".center(60))
        print("-" * 60)
        print()

        display_material_menu(materials_database)
        choice = input("Enter the material (or type 'exit' to quit): ").strip()
        if choice.lower() == "exit":
            break

        try:
            if choice.lower() == "custom":
                name = input("Enter the material name: ")
                density = float(input("Enter the density (kg/m^3): "))
                yield_strength = float(input("Enter the yield strength (in MPa): "))
                young_modulus = float(input("Enter the Young's modulus (in GPa): "))
                material: Material = Material(
                    name, MaterialProperties(density, yield_strength, young_modulus)
                )
                materials_database[material.name] = material
            elif choice in materials_database:
                material = materials_database[choice]
            else:
                raise ValueError(f"Material '{choice}' not found in the database.")

            force = float(input("Enter the applied force (in newtons): "))
            area = float(input("Enter the cross-sectional area (in square meters): "))
            orig_len = float(input("Enter the original length of the material (in meters): "))
            ch_len = float(input("Enter the change in length (in meters): "))

            test = StressTest(material, force, area, orig_len, ch_len)
            analysis.add_test(test)

            display_test_results(test)
            display_safety_analysis(test)

        except ValueError as e:
            print(f"Error: {e}")
            continue

    display_session_summary(analysis)
    print("Closing program...")


if __name__ == "__main__":
    main()