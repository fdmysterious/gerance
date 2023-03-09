"""
┌─────────────────────────────────┐
│ Test execution report dataclass │
└─────────────────────────────────┘

 Florian Dupeyron
 March 2022
"""

from dataclasses import dataclass, field
from typing      import Optional
from pathlib     import Path
from datetime    import datetime

from .test import Test

@dataclass
class Test_Status:
    desc: Test
    success: bool
    log_file: Path
    exc: Optional[Exception] = None


@dataclass
class Test_Report:
    name: str
    datetime: datetime

    results: List[Test_Status]
