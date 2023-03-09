"""
┌───────────────────────┐
│ Dataclasses for Tests │
└───────────────────────┘

 Florian Dupeyron
 January 2022
"""

from dataclasses  import dataclass, field
from typing       import List

@dataclass
class Test:
    id: str
    name: str
    version: str

    coverage: List[tuple[str,str]] = field(default_factory=list)
