"""
┌──────────────────────────┐
│ Save XML for test report │
└──────────────────────────┘

 Florian Dupeyron
 March 2022
"""

import logging
from lxml import etree

from gerance.model.test_report import (
    Test_Status,
    Test_Report
)

from pathlib import Path

log = logging.getLogger(__file__)

def to_xml(test_report: Test_Report, f_path: Path):
    f_path = Path(f_path)
    log.info(f"Save test report to {f_path}")
    
    # Create root node and general info
    t_root      = etree.Element("test-report")

    t_id        = etree.SubElement(t_root, "id")
    t_id.text   = test_report.name

    t_date      = etree.SubElement(t_root, "date")
    t_date.text = test_report.date.isoformat()

    # Create results
    t_results   = etree.SubElement(t_root, "results")
    for stat in test_report.results:
        t_exec = etree.SubElement(t_results, "test-execution")
        t_exec["result"] = 1 if stat.success else 0

        # Test information
        t_exec_id           = etree.SubElement(t_exec, "id")
        t_exec_id.text      = stat.desc.id

        t_exec_name         = etree.SubElement(t_exec, "name")
        t_exec_name.text    = stat.desc.name

        t_exec_version      = etree.SubElement(t_exec, "version")
        t_exec_version.text = stat.desc.version

        t_exec_logfile      = etree.SubElement(t_exec, "logfile")
        t_exec_logfile.text = stat.logfile
        
        if stat.exc is not None:
            t_exec_exc         = etree.SubElement(t_exec, "exception")
            t_exec_exc["type"] = type(stat.exc)
            t_exec_exc.text    = str(stat.exc)
        
    # Save tree to file
    et = etree.ElementTree(t_root)
    et.write(str(f_path), pretty_print=True)
