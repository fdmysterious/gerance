"""
┌─────────────────────────────────────────┐
│ Simple cache tools to accelerate things │
└─────────────────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

from dataclasses               import dataclass
from pathlib                   import Path
from typing                    import Dict, List, Tuple

from gerance.model.requirement import Requirement
from gerance.model.test        import Test

import gerance.views

import logging
import pickle

log = logging.getLogger(__file__)

@dataclass
class Gerance_Cache:
    """
    This class contains various views that accelerates
    some processing
    """
    req_list:         List[Requirement]
    test_list:        List[Test]

    req_dict:         Dict[str, Requirement]
    req_vitems_dict:  Dict[str, Tuple[str, ]]

    test_dict:        Dict[str, Test]
    test_vitems_dict: Dict[str, Test]


    # ┌────────────────────────────────────────┐
    # │ Save to pkl file                       │
    # └────────────────────────────────────────┘
    
    def save(self, fpath: Path):
        fpath = Path(fpath)
        log.info(f"Save gerance cache db to {fpath}")

        with open(fpath, "wb") as fhandle:
            pickle.dump(self, fhandle)


# ┌────────────────────────────────────────┐
# │ Load and create                        │
# └────────────────────────────────────────┘

def load(fpath: Path):
    fpath = Path(fpath)
    log.info(f"load gerance cache db from {fpath}")

    # Load pickle stuff
    with open(fpath, "rb") as fhandle:
        return pickle.load(fhandle)


def create(reqs_path: Path, tests_path: Path, requirement_file_module: any, test_file_module: any):
    reqs_path  = Path(reqs_path )
    tests_path = Path(tests_path)

    log.info(f"Create gerance db using following paths: ")
    log.info(f"- reqs_path:  {reqs_path}"                )
    log.info(f"- tests_path: {tests_path}"               )

    req_list  = list(requirement_file_module.load_from_dir(reqs_path))
    test_list = list(test_file_module.load_from_dir(tests_path))

    return Gerance_Cache(
        req_list        = req_list,
        test_list       = test_list,

        req_dict        = dict(gerance.views.build_req_dict        (req_list )),
        req_vitems_dict = dict(gerance.views.build_req_vitems_dict (req_list )),

        test_dict       = dict(gerance.views.build_test_dict       (test_list)),
        test_vitems_dict= dict(gerance.views.build_test_vitems_dict(test_list))
    )
