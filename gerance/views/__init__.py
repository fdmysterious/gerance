"""
┌─────────────────────────┐
│ Various views for stuff │
└─────────────────────────┘

 Florian Dupeyron
 May 2022
"""

from typing import List

from gerance.model.requirement import Requirement
from gerance.model.test        import Test


# ┌────────────────────────────────────────┐
# │ Views for requirements                 │
# └────────────────────────────────────────┘

def __visit_req_vitems(req_list: List[Requirement]):
    for req in req_list:
        for req_vitem in req.validation_items:
            yield req, req_vitem


def build_req_vitems_dict(req_list: List[Requirement]):
    return {
        req_vitem.id: {
            "req_id": req.id,
            "req_name": req.name,
            "req_version": req.version,

            "valid_desc": req_vitem.desc
        }

        for req, req_vitem in __visit_req_vitems(req_list)
    }


def build_req_dict(req_list: List[Requirement]):
    return {req.id: req for req in req_list}


# ┌────────────────────────────────────────┐
# │ Views for tests                        │
# └────────────────────────────────────────┘

def __visit_test_vitems(test_list: List[Test]):
    for test in test_list:
        for test_vitem in test.coverage:
            yield test, test_vitem


def build_test_dict(test_list: List[Test]):
    return {test.id: test for test in test_list}


def build_test_vitems_dict(test_list: List[Test]):
    res = dict()
    for test, test_vitem in __visit_test_vitems(test_list):
        res[test_vitem[0]] = res.get(test_vitem[0], list()) + [(test_vitem[1], test)]
    
    return res
