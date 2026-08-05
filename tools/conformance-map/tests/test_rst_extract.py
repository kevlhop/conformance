# Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
# Security Alliance (GEISA), a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0. See LICENSE.

"""Tests for RST requirement extraction."""

from pathlib import Path

import yaml

from geisa_conformance_map.cli import main
from geisa_conformance_map.rst_extract import extract_candidates

FIXTURE = Path(__file__).parent / "fixtures" / "specification"


def test_extracts_reviewable_blocks_with_context() -> None:
    """LEE extraction should retain matches, sections, lists, and case."""

    data = extract_candidates(FIXTURE, "LEE")

    assert data["pillar"] == "LEE"
    assert data["candidate_count"] == 9
    assert data["keyword_occurrence_count"] == 10
    assert data["noncanonical_keyword_count"] == 2

    candidates = data["candidates"]

    nonroot_candidate = next(
        candidate
        for candidate in candidates
        if candidate["requirement"]["source_text"]
        == "Applications SHALL not run as root."
    )
    assert nonroot_candidate["type"] == "requirement-candidate"
    assert nonroot_candidate["source"]["document"] == "Application Isolation"
    assert nonroot_candidate["source"]["section"] == "Application Isolation"
    assert nonroot_candidate["requirement"]["matches"][0] == {
        "level": "SHALL NOT",
        "source_keyword": "SHALL not",
        "noncanonical_case": True,
        "start": 13,
        "end": 22,
    }

    grouped_candidate = next(
        candidate
        for candidate in candidates
        if candidate["requirement"]["source_text"]
        == "Platform implementations MUST provide:"
    )
    assert grouped_candidate["children"] == [
        {
            "text": "a shared base image",
            "children": [{"text": "a hardened base image"}],
        },
        {"text": "application image support"},
    ]

    aggregate_candidate = next(
        candidate
        for candidate in candidates
        if candidate["requirement"]["source_text"]
        == (
            "Platform implementations MUST retain application state and SHALL NOT "
            "discard it before a requested reset."
        )
    )
    assert [
        match["level"] for match in aggregate_candidate["requirement"]["matches"]
    ] == [
        "MUST",
        "SHALL NOT",
    ]

    tmp_candidate = next(
        candidate
        for candidate in candidates
        if candidate.get("context", {}).get("list_path") == ["/tmp"]
    )
    assert tmp_candidate["requirement"]["source_text"] == (
        "MUST be limited in size as described in the deployment manifest"
    )

    lowercase_candidate = next(
        candidate
        for candidate in candidates
        if "must bring their own" in candidate["requirement"]["source_text"]
    )
    assert lowercase_candidate["requirement"]["matches"][0]["noncanonical_case"] is True

    nested_candidate = next(
        candidate
        for candidate in candidates
        if candidate["source"]["path"] == "source/lee/nested/storage.rst"
    )
    assert nested_candidate["requirement"]["source_text"] == (
        "Persistent storage MUST survive application restarts."
    )

    note_candidate = next(
        candidate
        for candidate in candidates
        if "infer behavior" in candidate["requirement"]["source_text"]
    )
    assert note_candidate["context"]["admonition"] == {
        "type": "note",
        "title": None,
    }

    reserved_candidate = next(
        candidate
        for candidate in candidates
        if "reject operations" in candidate["requirement"]["source_text"]
    )
    assert reserved_candidate["context"]["admonition"] == {
        "type": "admonition",
        "title": "Status: Reserved for Future Definition",
        "classes": ["tbd-section"],
    }


def test_cli_writes_yaml(tmp_path: Path) -> None:
    """The CLI should write generated candidates as YAML."""

    output = tmp_path / "lee.yaml"

    result = main(
        [
            "extract-rst",
            "--source",
            str(FIXTURE),
            "--pillar",
            "LEE",
            "--output",
            str(output),
        ]
    )

    assert result == 0

    data = yaml.safe_load(output.read_text(encoding="utf-8"))

    assert data["candidate_count"] == 9
    assert data["keyword_occurrence_count"] == 10
    assert data["noncanonical_keyword_count"] == 2
