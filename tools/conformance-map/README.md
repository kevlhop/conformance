<!--
Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
Security Alliance (GEISA), a Series of LF Projects, LLC

Licensed under the Apache License, Version 2.0. See LICENSE.
-->

# GEISA Conformance Map

GEISA Conformance Map will connect requirements in the GEISA specification and
schemas to the tests in this repository.

It is intended to show:

- what a selected GEISA version requires for each conformance pillar
- whether a requirement comes from specification text, protobufs, JSON Schemas,
  or profiles
- which current Cukinia tests cover each requirement
- what is missing or only partially covered
- what changed between a release and current development

LEE and API are the initial focus. ADM and VEE are intentionally paused while
coverage of the first two pillars is improved.

## Approach

The tool will use existing projects where possible instead of building a full
requirements system from scratch:

- Sphinx and Docutils for parsing the existing RST specification
- Sphinx-Needs for linked requirement and test views where it fits
- `protoc` descriptor sets for protobuf structure
- Buf for protobuf linting and compatibility checks
- `jsonschema` or `check-jsonschema` for JSON Schema validation

GEISA-specific code will handle:

- resolving sources and recording exact revisions
- extracting requirement candidates
- applying reviewed IDs and decisions
- normalizing contract rules
- scanning Cukinia tests
- suggesting and storing approved mappings
- determining applicability by pillar, profile, and advertised capability
- comparing releases with current development
- generating reports and optional test scaffolding

## Intended workflow

A normal run will:

1. Resolve a release, commit, `latest`, or local workspace to an exact source state
2. Extract requirement candidates and machine-defined contract rules
3. Apply the reviewed decisions under `requirements/`
4. Scan the existing Cukinia tests
5. Suggest mappings and identify gaps
6. Generate reports under `build/conformance-map/`

Reviewed release baselines may be committed under `requirements/baselines/`.
Results from current development or dirty workspaces remain generated output.

## Planned commands

The final command names may change as the initial implementation is tested.

```text
geisa-conformance-map inventory --target tag:v0.9.0
geisa-conformance-map compare --baseline tag:v0.9.0 --target latest
geisa-conformance-map report --target latest
geisa-conformance-map scaffold --pillar LEE
```

## Repository layout

- `requirements/` contains reviewed project data and release baselines
- `tools/conformance-map/` contains the implementation and committed docs
- `build/conformance-map/` contains generated output and is ignored by Git

## Local setup

Create the local development environment:

```sh
tools/conformance-map/setup-venv.sh
source tools/conformance-map/.venv/bin/activate

## Status

General structure and initial documentation are in place, but implementation
has not yet started.
