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

