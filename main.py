#!/usr/bin/env python3
"""Entry point for the news-image-20261121 submission.

The finished picture lives in this repository as entry.png. This program
only carries that file over to the output directory the grader provides,
so the image the judge sees is exactly the one committed here.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    # The grader sets MAKEFUN_OUTPUT_DIR; fall back to /output.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
