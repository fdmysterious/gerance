"""
Parse gherkin test description file

Florian Dupeyron
October 2022
"""

import logging
import re

from pathlib            import Path
from gerance.model.test import (
    Test
)

from gherkin_paperwork  import feature_file

__REG_COVERAGE = re.compile(r"^@covers\.(.*?)(?:\[(.*?)\])?$")

log = logging.getLogger(__file__)

def parse(f_path):
    """
    Parses a gherkin feature file.
    Note: Coverage is computed through scenario tags, starting with "covers.XXXX[version]",
    for instance: "covers.my_vitem_id[2.22]"

    :return: A list of parsed tests (corresponding to scenario objects)
    """


    log.debug(f"Load gherkin feature from {f_path}")

    f_path = Path(f_path)

    # Parse feature file
    feature = feature_file.from_file(f_path)

    result  = list()
    def traverse(root, obj):
        if isinstance(obj, feature_file.Rule) or isinstance(obj, feature_file.Feature):
            for c in obj.children:
                yield from traverse(root, c)

        elif isinstance(obj, feature_file.Scenario):
            # This should return all non null match objects
            mt_objs = filter(lambda x: x is not None, map(lambda x: __REG_COVERAGE.match(x.name), obj.tags))

            # Transforms the list of match objects to tuples containing the validation item ID and version
            coverage = list(map(lambda x: (x.group(1) or None, x.group(2) or None,), mt_objs))

            # Create and return the scenario object
            yield Test(
                id       = f"{f_path.name}:{obj.location.line}",
                name     = obj.name,
                version  = None, # FIXME How to indicate test version ? Tag, description text, title magic, or git tag ?
                coverage = coverage
            )

        else:
            pass
    
    return traverse(feature, feature)