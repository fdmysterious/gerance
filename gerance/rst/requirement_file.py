"""
Simple parser for requirements files in RST format

Florian Dupeyron
October 2022
"""

import docutils
import logging

from docutils import nodes
from docutils import frontend
from docutils import transforms
from docutils import utils

from docutils.parsers    import rst
from docutils.transforms import frontmatter

from pathlib  import Path

from gerance.model.requirement import (
    Requirement,
    Requirement_Validation_Item
)

log = logging.getLogger(__file__)

# ----------------------- Visitors

class ReqHeaderVisitor(nodes.NodeVisitor):
    def __init__(self, document):
        super().__init__(document)

        # Extracted info. variables
        self.version           = None
        self.req_id            = None
        self.validation_points = None


    def unknown_visit(self, node):
        pass


    def visit_field(self, node):
        simple_fields = {
            "Version": "version",
            "Req-ID": "req_id"
        }

        # Get field nodes
        n_field_name = node.next_node(nodes.field_name)
        n_field_body = node.next_node(nodes.field_body)

        if n_field_name is None:
            raise ValueError("No field name")
        elif n_field_body is None:
            raise ValueError("No field body")

        # Get field info.
        field_name = n_field_name.astext()

        # Check for simple fields
        if field_name in simple_fields:
            setattr(self, simple_fields[field_name], n_field_body.astext())


# ----------------------- Parse function

def parse(f_path):
    # Parse document
    parser   = rst.Parser()
    settings = frontend.get_default_settings(rst.Parser)
    document = utils.new_document(str(f_path), settings)

    parser.parse(f_path.read_text(), document)

    # Apply transforms
    doc_transform = frontmatter.DocTitle(document)
    doc_transform.apply()

    # Find title
    title_idx = document.first_child_matching_class(nodes.title)
    if title_idx is None:
        raise ValueError("No name for requirement")

    req_name = document[title_idx].astext()

    # Find header fields
    fields_idx = document.first_child_matching_class(nodes.field_list)
    if fields_idx is None:
        raise ValueError("Missing header field list")

    main_fields = document[fields_idx]

    # Visit main fields
    visitor = ReqHeaderVisitor(document)
    main_fields.walk(visitor)

    # Check extracted info.
    if visitor.req_id is None:
        raise ValueError("Missing Req-ID header field")

    return Requirement(
        id      = visitor.req_id,
        name    = req_name,
        version = visitor.version,

        validation_items = [
            Requirement_Validation_Item(id=visitor.req_id, desc=req_name)
        ]
    )

# ----------------------- Load from directory

def load_from_dir(dir_path: Path):
    log.info(f"Load requirements from {dir_path}")
    
    # Check dir_path
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise NotADirectoryError(dir_path)

    # Process all XML files
    return map(parse, dir_path.glob("*.rst"))
