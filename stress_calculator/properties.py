from dataclasses import dataclass
from properties import MaterialProperties


@dataclass
class MaterialProperties:

    density: float
    yield_strength: float
    young_modulus: float

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be greater than zero")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be greater than zero")
        if self.young_modulus <= 0:
            raise ValueError("Young's modulus must be greater than zero")
