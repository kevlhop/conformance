# Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
# Security Alliance (GEISA), a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0. See LICENSE.

"""Command-line entry point for GEISA Conformance Map."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from geisa_conformance_map import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="geisa-conformance-map",
        description="Map GEISA requirements and contract rules to tests",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
