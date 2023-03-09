"""
┌─────────────────────────────────┐
│ Parse XML test description file │
└─────────────────────────────────┘

 Florian Dupeyron
 February 2022
"""

import logging

from lxml    import etree
from pathlib import Path

from gerance.model.test import (
    Test
)

log = logging.getLogger(__file__)

def __parse_test_coverage(el: etree.Element):
    if el.tag != "item": raise ValueError(f"Expected 'item' tag, got '{el.tag}'")

    el_id      = el.get("id"     )
    el_version = el.get("version")

    if el_id      is None: raise ValueError("Missing 'id' attribute")
    if el_version is None: raise ValueError("Missing 'version' attribute")

    return (el_id, el_version,)

def parse(f_path):
    log.debug(f"Process test data from {f_path}")
    dom = etree.parse(str(f_path))

    t_root = dom.getroot()

    if t_root.tag != "test": raise ValueError(f"Expected 'test' root tag, got '{t_root.tag}'")

    # Get key tags
    t_id      = t_root.find("id"     )
    t_version = t_root.find("version")
    t_name    = t_root.find("name"   )

    if t_id      is None: raise ValueError("Missing 'id' tag"     )
    if t_version is None: raise ValueError("Missing 'version' tag")
    if t_name    is None: raise ValueError("Missing 'name' tag"   )

    el_id      = str(t_id.xpath("string()"))
    el_version = str(t_version.xpath("string()"))
    el_name    = str(t_name.xpath("string()"))

    # Create result element
    r = Test(
        id      = el_id,
        name    = el_name,
        version = el_version
    )

    # Parse coverage elements
    t_validation = t_root.find("validates")
    if t_validation is not None:
        r.coverage = [__parse_test_coverage(t_vitem) for t_vitem in t_validation.iter("item")]

    return r

def load_from_dir(dir_path: Path):
    log.info(f"Load tests from {dir_path}")
    
    # Check dir_path
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise NotADirectoryError(dir_path)

    # Process all XML files
    return map(parse, dir_path.glob("*.xml"))
