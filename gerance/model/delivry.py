"""
┌───────────────────────────────┐
│ Delivry description dataclass │
└───────────────────────────────┘

 Florian Dupeyron
 January 2022
"""

from dataclasses import dataclass
from typing      import Set


@dataclass
class Delivry_Description:
    name: str
    validation_requirements: Set[str]
