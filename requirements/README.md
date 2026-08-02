<!--
Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
Security Alliance (GEISA), a Series of LF Projects, LLC

Licensed under the Apache License, Version 2.0. See LICENSE.
-->

# Conformance Map Data

This directory contains the reviewed data used by GEISA Conformance Map.

The map connects:

- requirements found in the GEISA specification
- contract rules defined by protobufs, JSON Schemas, and profiles
- Cukinia tests that provide evidence for those requirements and rules

Generated candidates, reports, and temporary source snapshots are written under
`build/conformance-map/` and are not committed.

## Layout

- `review/` contains decisions made while reviewing extracted requirements
- `mappings/` connects approved requirements and contract rules to tests
- `baselines/` stores reviewed snapshots for released GEISA versions
- `schemas/` validates the files maintained in this directory

LEE and API are the initial focus. ADM and VEE may be inventoried, but their
test coverage work is currently parked.

## Workflow

1. Select a released GEISA version, exact commit, or current development source
2. Extract requirements and contract rules
3. Review new or changed results
4. Map approved items to existing tests
5. Identify missing or partial coverage
6. Generate reports or optional test scaffolding

The reviewed files in this directory are the project record. Generated output
can be recreated as needed from the selected sources.
