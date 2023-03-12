"""
==========================================
Simple tools for requirements in PDF files
==========================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: March 2023
"""

import logging
import re

from pathlib import Path

from gerance.model.requirement import (
    Requirement,
    Requirement_Validation_Item
)

from pypdf import PdfReader

log = logging.getLogger(__file__)

def parse(
    f_path: Path,
    requirement_regex: str
):
    """
    Processes a PDF file for requirements.

    The requirements regex should have the following matching groups:
        - req_id: Requirement ID
        - req_name: Requirement Name
        - req_version: Requirement version

    So, for example: let's suppose the following requirement format:

        [REQ-0001-A] Requirement title

    This leads to the following regex:

        "\[(?P<req_id>REQ-[0-9]{4})-(?P<req_version>[A-Z])\]\s*(?P<req_name>.*?)$"

    :param f_path: Path to input PDF file
    :param requirement_regex: Regex for requirement ID, name and version
    """

    if isinstance(requirement_regex, str):
        requirement_regex = re.compile(requirement_regex)

    log.info(f"Process PDF file for requirements: {f_path}")

    reader = PdfReader(str(f_path))
    reqs   = []

    for idx, page in enumerate(reader.pages):
        log.debug(f"Process page {idx+1}")

        txt = page.extract_text()
        for line in txt.split("\n"):
            for mt in requirement_regex.finditer(line):
                req_id      = mt.group("req_id"     )
                req_version = mt.group("req_version")
                req_name    = mt.group("req_name"   )

                reqs.append(Requirement(
                    id      = req_id,
                    name    = req_name,
                    version = req_version,

                    validation_items = [
                        Requirement_Validation_Item(
                            id   = req_id,
                            desc = f"{req_name} - {f_path}:{idx+1}",
                        )
                    ]
                ))

    return reqs

