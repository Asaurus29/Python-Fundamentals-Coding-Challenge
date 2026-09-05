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
