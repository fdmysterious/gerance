"""
┌────────────────────────────────────────┐
│ Parse XML requirement description file │
└────────────────────────────────────────┘

 Florian Dupeyron
 January 2022
"""

import logging

from lxml    import etree
from pathlib import Path

from gerance.model.requirement import (
    Requirement_Validation_Item,
    Requirement
)


log = logging.getLogger(__file__)

def __parse_valid_item(el: etree.Element):
    """
    Parse requirement items
    """

    if el.tag != "item": raise ValueError(f"Expected 'item' tag, got el={el}")

    # Get element id
    el_id = el.get("id")
    if el_id is None: raise ValueError(f"Missing 'id' attribute on element {el}")

    # Get element description
    el_desc = None
    t_desc = el.find("desc")
    if t_desc is not None:
        el_desc = t_desc.xpath("string()")

    return Requirement_Validation_Item(
        id   = el_id,
        desc = el_desc
    )

def parse(f_path):
    log.debug(f"Process requirement data from {f_path}")
    dom    = etree.parse(str(f_path))
    t_root = dom.getroot()

    # Get key tags
    if t_root.tag != "requirement": raise ValueError(f"Expected 'requirement' root tag, got el={t_root}")

    t_id       = t_root.find("id"      )
    t_version  = t_root.find("version" )
    t_name     = t_root.find("name"    )
    t_parts    = t_root.find("parts"   )

    if t_id      is None: raise ValueError("Missing 'id' tag"     )
    if t_version is None: raise ValueError("Missing 'version' tag")
    if t_name    is None: raise ValueError("Missing 'name' tag"   )

    # Get info text
    el_id      = str(t_id.xpath("string()"     ))
    el_version = str(t_version.xpath("string()"))
    el_name    = str(t_name.xpath("string()"   ))

    # Create item
    req = Requirement(
        id           = el_id,
        version      = el_version,
        name         = el_name,
    )

    # Add requirement validation items
    t_validation = t_root.find("validation")
    if t_validation is not None:
        for t_item in t_validation.iter("item"):
            req.validation_items.append(__parse_valid_item(t_item))

    return req


def load_from_dir(dir_path: Path):
    log.info(f"Load requirements from {dir_path}")
    
    # Check dir_path
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise NotADirectoryError(dir_path)

    # Process all XML files
    return map(parse, dir_path.glob("*.xml"))
