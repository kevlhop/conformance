#!/usr/bin/env bash
# Copyright 2025-2026, Contributors to the Grid Edge Interoperability &
# Security Alliance (GEISA), a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0. See LICENSE.

set -euo pipefail

TOOL_DIR="$(
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
    pwd
)"

VENV_DIR="${TOOL_DIR}/.venv"

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -e "${TOOL_DIR}[dev]"

echo
echo "Conformance Map environment is ready"
echo "Activate it with:"
echo
echo "  source tools/conformance-map/.venv/bin/activate"
