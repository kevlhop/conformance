# Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
# Security Alliance (GEISA), a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0. See LICENSE.

"""Command-line entry point for GEISA Conformance Map."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from geisa_conformance_map import __version__
from geisa_conformance_map.rst_extract import extract_candidates, write_candidates


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

    commands = parser.add_subparsers(dest="command")

    extract_rst = commands.add_parser(
        "extract-rst",
        help="extract requirement candidates from GEISA RST sources",
    )
    extract_rst.add_argument(
        "--source",
        required=True,
        type=Path,
        help="path to a GEISA specification checkout",
    )
    extract_rst.add_argument(
        "--pillar",
        required=True,
        choices=("API", "LEE"),
        help="conformance pillar to extract",
    )
    extract_rst.add_argument(
        "--output",
        required=True,
        type=Path,
        help="generated YAML output path",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract-rst":
        data = extract_candidates(args.source, args.pillar)
        write_candidates(data, args.output)
        print(
            f"Wrote {data['candidate_count']} {data['pillar']} candidates "
            f"to {args.output}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
