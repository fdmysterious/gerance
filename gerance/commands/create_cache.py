"""
┌──────────────────────────┐
│ Create cache for gerance │
└──────────────────────────┘

 Florian Dupeyron
 May 2022
"""

import argparse
import logging
import os

import gerance.cache

from pathlib import Path

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
    logging.basicConfig(level=logging.DEBUG if os.environ.get("DEBUG",0) else logging.INFO)

    parser = argparse.ArgumentParser(description="Create gerance cache from XML folders"      )
    parser.add_argument("folder_req"  , type=dir_path, help="Path containing XML requirements")
    parser.add_argument("folder_tests", type=dir_path, help="Path containing XML tests"       )
    parser.add_argument("output_file" , type=dir_file, help="Path to output pkl file"         )
    
    args = parser.parse_args()

    cache = gerance.cache.create(args.folder_req, args.folder_tests)
    cache.save(args.output_file)
