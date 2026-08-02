# Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
# Security Alliance (GEISA), a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0. See LICENSE.

"""Smoke tests for the Conformance Map command line."""

from geisa_conformance_map.cli import main


def test_empty_command_succeeds() -> None:
    """The initial command should load successfully."""

    assert main([]) == 0
