# material.py

from dataclasses import dataclass
from typing import Optional

# Import from our own modules
from properties import MaterialProperties


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
        if not isinstance(other, StressTest):
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

#properties.py

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
