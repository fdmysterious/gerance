"""
┌───────────────────────────────┐
│ Base classes for requirements │
└───────────────────────────────┘

 Florian Dupeyron
 January 2022
"""

from dataclasses import dataclass, field
from typing      import List, Optional

@dataclass
class Requirement_Validation_Item:
    id: str
    desc: Optional[str]


    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Requirement:
    id: str
    name: str
    version: str

    validation_items: List[Requirement_Validation_Item] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["validation_items"]

        return cls(**dd2,
            validation_items=[
                Requirement_Validation_Item.from_dict(x) for x in data["validation_items"]
            ]
        )
