"""
┌─────────────────────────────┐
│ Various reports for Gerance │
└─────────────────────────────┘

 Florian Dupeyron
 February 2022
"""

import logging
#import pandas   as pd

from functools import reduce

from typing import List

from gerance.cache import Gerance_Cache

from gerance.model.requirement import (
    Requirement,
    Requirement_Validation_Item
)

from gerance.model.test        import (
    Test
)

log = logging.getLogger(__file__)

from pprint import pprint


# ┌────────────────────────────────────────┐
# │ Test coverage report                   │
# └────────────────────────────────────────┘

def test_coverage(test: Test, cache: Gerance_Cache):
    """
    Return a dataframe indicating which requirements are covered by a test:
        { "req_id": "...", "cov_ver": "...", "type": "full"|"partial", "req_ver": "..."}

        - cov_ver is the requirement. version covered by the test
        - req_ver is the current requirement version
    """


    # Build req_vitems dict and req_dict
    #req_vitems_dict            = build_req_vitems_dict(req_list)
    #req_dict                   = build_req_dict       (req_list)

    # Extract covered validation items IDs from test
    covered_vitems_ids         = set(map(lambda x: x[0], test.coverage))

    # Build covered and uncovered dicts
    covered_vitems             = {k: cache.req_vitems_dict[k] for k   in covered_vitems_ids            if k in cache.req_vitems_dict}
    uncovered_vitems           = {k: v                        for k,v in cache.req_vitems_dict.items() if k not in covered_vitems_ids}

    # List req ids that are not or partially covered
    # use of set: removes duplicates

    covered_reqs_ids           = set(v["req_id"] for k,v in covered_vitems.items()  )
    partial_uncovered_reqs_ids = set(v["req_id"] for k,v in uncovered_vitems.items())

    # Build final list
    return [
        {
            "req_id" : r_id,
            "cov_ver": "...",
            "type"   : "partial" if r_id in partial_uncovered_reqs_ids else "full",
            "req_ver": cache.req_dict[r_id].version
        }

        for r_id in covered_reqs_ids
    ]


# ┌────────────────────────────────────────┐
# │ Requirement coverage report            │
# └────────────────────────────────────────┘

def req_vitem_coverage(req_vitem: Requirement_Validation_Item, cache: Gerance_Cache):
    """
    Returns the test coverage for the given validation item
    """

    return cache.test_vitems_dict.get(req_vitem.id, [])


def req_coverage(req: Requirement, cache: Gerance_Cache):
    """
    Gives the coverage for the given requirement:

    {
        "<valid_id>": {
            "description": "...",
            "tests": [
                {
                    "id":             "test_id",
                    "version":        "test_version",
                    "tested_version": "tested_version"
                },

                ...
            ]
        }
    }
    """

    return {
        req_vitem.id: {
            "description": req_vitem.desc,
            "tests": [
                {
                    "id":             test.id,
                    "version":        req.version,
                    "tested_version": tested_version
                }

                for tested_version, test in cache.test_vitems_dict.get(req_vitem.id, [])
            ]
        }

        for req_vitem in req.validation_items
    }


def reqlist_coverage(req_list: List[Requirement], cache: Gerance_Cache):
    """
    Returns three lists for coverage:
        - Covered items
        - Non covered items
        - Version mismatch
    """

    covered_items   = dict()
    uncovered_items = dict()
    mismatch_items  = dict()

    for req in req_list:
        for req_vitem in req.validation_items:
            cov_tests = req_vitem_coverage(req_vitem, cache)

            # Item is not covered
            if not cov_tests:
                if not req.id in uncovered_items:
                    uncovered_items[req.id] = set()

                uncovered_items[req.id].add(req_vitem.id)

            else:
                for cov in cov_tests:
                    # Version mismatch
                    if cov[0] != req.version:
                        if not req.id in mismatch_items:
                            mismatch_items[req.id] = dict()

                        mismatch_items[req.id][req_vitem.id] = mismatch_items[req.id].get(req_vitem.id, []) + [{"id": cov[1].id, "version": cov[1].version, "tested_version": cov[0], "req_version": req.version}]

                    # Item is covered
                    else:
                        if not req.id in covered_items:
                            covered_items[req.id] = dict()

                        covered_items[req.id][req_vitem.id] = covered_items[req.id].get(req_vitem.id, []) + [{
                            "id": cov[1].id, "version": cov[1].version, "tested_version": cov[0], "req_version": req.version
                        }]
                

    return covered_items, uncovered_items, mismatch_items

# ┌────────────────────────────────────────┐
# │ Coverage report                        │
# └────────────────────────────────────────┘

#def req_coverage(req_list: List[Requirement], test_list: List[Test]):
#    """
#    Returns three dataframes reporting coverage status
#        - a DataFrame indicating covered requirement validation items
#        - a DataFrame indicating non covered requirement validation items
#        - a DataFrame indicating covered requirement validation items but with version mismatch
#    """
#
#    # Build requirement vitems df
#    log.debug("Build requirements vitems df")
#
#    r_records = []
#    for req in req_list:
#        for req_vitem in req.validation_items:
#            r_records.append({
#                "req_id"     : req.id,
#                "req_name"   : req.name,
#                "req_version": req.version,
#
#                "valid_id"   : req_vitem.id,
#                "valid_desc" : req_vitem.desc
#            })
#    
#    req_vitems_df = __build_req_vitems_df(req_list)
#
#    # Build test vitems df
#    log.debug("Build test vitems df")
#
#    t_records = []
#    for test in test_list:
#        for valid_id, req_ver in test.coverage:
#            t_records.append({
#                "test_id"     : test.id,
#                "test_name"   : test.name,
#                "test_version": test.version,
#                "valid_id"    : valid_id,
#                "test_req_ver": req_ver
#            })
#    
#    test_vitems_df = pd.DataFrame.from_records(t_records)
#
#    # Match
#    covered_df      = req_vitems_df.merge(test_vitems_df, left_on=["valid_id", "req_version"], right_on=["valid_id", "test_req_ver"], how="inner")
#    covered_all_df  = req_vitems_df.merge(test_vitems_df, left_on=["valid_id"]               , right_on=["valid_id"], how="inner")
#
#    # Find covered valid_id (correct or version mismatch)
#    covered_vitems  = covered_all_df.valid_id.unique()
#    non_covered_df  = req_vitems_df[~req_vitems_df["valid_id"].isin(covered_vitems)]
#
#    ver_mismatch_df = covered_all_df[covered_all_df.req_version != covered_all_df.test_req_ver]
#
#    return covered_df, non_covered_df, ver_mismatch_df
#
