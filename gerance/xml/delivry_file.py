"""
┌────────────────────────────────────┐
│ Parse XML delivry description file │
└────────────────────────────────────┘

 Florian Dupeyron
 February 2022
"""

import logging

from lxml    import etree
from pathlib import Path

from gerance.model.delivry import (
    Delivry_Description
)

log = logging.getLogger(__file__)

def parse(f_path: Path):
    log.info(f"Process delivry data from {f_path}")
    dom    = etree.parse(str(f_path))
    t_root = dom.getroot()

    # Get key tags
    if t_root.tag != "delivry": raise ValueError(f"Root tag of {f_path} delivry description file is not 'delivry' but '{t_root.tag}'")

    t_name = t_root.find("name")
    if t_name is None: raise ValueError("Missing 'name' tag")

    d_name = t_name.xpath("string()")
    d_reqs = set()

    t_vreqs = t_root.find("validation-requirements")
    if t_vreqs is None:
        raise ValueError(f"Missing 'validation-requirements' tag")

    for t_req in t_vreqs.findall("req"):
        req_id = t_req.get("id")
        if req_id is None:
            raise ValueError(f"req tag don't have the 'id' attribute")

        d_reqs.add(req_id)

    return Delivry_Description(
        name                    = d_name,
        validation_requirements = d_reqs
    )

