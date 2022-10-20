"""
┌───────────────────────────────┐
│ Generate coverage report file │
└───────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

import argparse
import logging
import os

import gerance.cache
import gerance.reports
from   gerance.xml import delivry_file

from pathlib import Path

from lxml import etree

# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(path):
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"{str(path)} is not a valid path")
    return p

def dir_file(path):
    p = Path(path)
    if p.is_dir():
        raise argparse.ArgumentTypeError(f"{str(path)} is a folder")
    return p

if __name__ == "__main__":
    log = logging.getLogger(__file__)

    logging.basicConfig(level=logging.DEBUG if os.environ.get("DEBUG",0) else logging.INFO)

    parser = argparse.ArgumentParser(description="Create coverage report")

    parser.add_argument("folder_req"  ,    type=dir_path, help="Path containing XML requirements"                   )
    parser.add_argument("folder_tests",    type=dir_path, help="Path containing XML tests"                          )
    parser.add_argument("-d", "--delivry", type=dir_file, help="Optional path to delivry file"                      )
    parser.add_argument("-o", "--output" , type=str     , help="Path to the output file, writes to STDOUT otherwise")

    args     = parser.parse_args()

    # Create gerance cache
    cache    = gerance.cache.create(args.folder_req, args.folder_tests)

    # Get coverage information
    if args.delivry:
        log.info(f"Get coverage information with requirements from delivry {args.delivry}")
        delivry  = delivry_file.parse(args.delivry)
        reqlist  = [cache.req_dict[req_id] for req_id in delivry.validation_requirements]

    else:
        log.info("Get coverage information for all requirements")
        reqlist = cache.req_list

    covered_items, uncovered_items, mismatch_items = gerance.reports.reqlist_coverage(reqlist, cache)

    # Create report XML
    t_root = etree.Element("coverage-report")

    # Covered items
    t_covered_items = etree.SubElement(t_root, "covered-items")
    for req_id, req_vitems in covered_items.items():
        t_req = etree.SubElement(t_covered_items, "requirement", id=req_id, version=cache.req_dict[req_id].version)

        for vitem_id, vitem_infos in req_vitems.items():
            t_item = etree.SubElement(t_req, "item", id=vitem_id, description=cache.req_vitems_dict[vitem_id]["valid_desc"])

            for test in vitem_infos:
                t_covered_by = etree.SubElement(t_item, "covered-by", test=test["id"], version=test["version"])

    # Uncovered items
    t_uncovered_items = etree.SubElement(t_root, "uncovered-items")
    for req_id, req_vitems in uncovered_items.items():
        t_req = etree.SubElement(t_uncovered_items, "requirement", id=req_id, version=cache.req_dict[req_id].version)

        for vitem_id in req_vitems:
            t_item = etree.SubElement(t_req, "item", id=vitem_id, description=cache.req_vitems_dict[vitem_id]["valid_desc"])

    # Version mismatch items
    t_mismatch_items = etree.SubElement(t_root, "mismatch-items")
    for req_id, req_vitems in mismatch_items.items():
        t_req = etree.SubElement(t_mismatch_items, "requirement", id=req_id, version=cache.req_dict[req_id].version)

        for vitem_id, vitem_infos in req_vitems.items():
            t_item = etree.SubElement(t_req, "item", id=vitem_id, description=cache.req_vitems_dict[vitem_id]["valid_desc"])

            for test in vitem_infos:
                t_mismatch = etree.SubElement(t_item, "mismatch", test=test["id"], version=test["version"], covers=test["tested_version"], expected=test["req_version"])
            

    # Output report
    et = etree.ElementTree(t_root)

    if args.output:
        log.info(f"Write result report to {args.output}")
        et.write(str(args.output), pretty_print=True)
    else:
        log.info("Write result report to stdout")
        print(etree.tostring(t_root, pretty_print=True))
