#!/usr/bin/env bash
# Integration tests for the oci_mirror role.
# Runs ansible-playbook against oci_mirror.yml using --local mode (no Docker).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ansible-playbook "${SCRIPT_DIR}/oci_mirror.yml" "$@"
