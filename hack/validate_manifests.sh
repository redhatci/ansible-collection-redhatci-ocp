#!/usr/bin/env bash
# validate_manifests.sh — validate oc-mirror v2 output manifests
#
# Usage: validate_manifests.sh <directory>
#
# Validates all *.yaml files in <directory>:
#   - apiVersion, kind, and metadata.name must be non-empty strings
#   - status must not be an empty dict ({})
#   - Kind-specific spec field checks:
#       ImageDigestMirrorSet  : spec.imageDigestMirrors non-empty list
#       ImageTagMirrorSet     : spec.imageTagMirrors non-empty list
#       CatalogSource         : spec.sourceType and spec.image non-empty strings
#       ClusterCatalog        : spec.source must be defined
#       UpdateService         : spec.graphDataImage and spec.releases non-empty strings
#
# Exit 0 on success, exit 1 with ERROR lines on stderr on any failure.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <manifest-directory>" >&2
    exit 1
fi

MANIFEST_DIR="$1"

if [[ ! -d "${MANIFEST_DIR}" ]]; then
    echo "ERROR: directory not found: ${MANIFEST_DIR}" >&2
    exit 1
fi

python3 - "${MANIFEST_DIR}" <<'PYEOF'
import sys
import os
import glob
import yaml

def validate_manifest(path):
    errors = []
    basename = os.path.basename(path)

    with open(path, "r", encoding="utf-8") as fh:
        try:
            doc = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            return [f"{basename}: YAML parse error: {exc}"]

    if not isinstance(doc, dict):
        return [f"{basename}: top-level document is not a mapping"]

    # --- Common required fields ---
    for field in ("apiVersion", "kind"):
        val = doc.get(field)
        if not val or not str(val).strip():
            errors.append(f"{basename}: '{field}' is missing or empty")

    metadata = doc.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("name", "").strip():
        errors.append(f"{basename}: 'metadata.name' is missing or empty")

    # --- status must not be an empty dict ---
    if "status" in doc and doc["status"] == {}:
        errors.append(
            f"{basename}: 'status' is an empty dict — this indicates a "
            "serialization defect in the manifest output"
        )

    kind = doc.get("kind", "")
    spec = doc.get("spec", {}) or {}

    # --- Kind-specific checks ---
    if kind == "ImageDigestMirrorSet":
        mirrors = spec.get("imageDigestMirrors")
        if not mirrors or not isinstance(mirrors, list) or len(mirrors) == 0:
            errors.append(
                f"{basename}: 'spec.imageDigestMirrors' is missing or empty "
                "(ImageDigestMirrorSet)"
            )

    elif kind == "ImageTagMirrorSet":
        mirrors = spec.get("imageTagMirrors")
        if not mirrors or not isinstance(mirrors, list) or len(mirrors) == 0:
            errors.append(
                f"{basename}: 'spec.imageTagMirrors' is missing or empty "
                "(ImageTagMirrorSet)"
            )

    elif kind == "CatalogSource":
        if not spec.get("sourceType", "").strip():
            errors.append(
                f"{basename}: 'spec.sourceType' is missing or empty (CatalogSource)"
            )
        if not spec.get("image", "").strip():
            errors.append(
                f"{basename}: 'spec.image' is missing or empty (CatalogSource)"
            )

    elif kind == "ClusterCatalog":
        if "source" not in spec:
            errors.append(
                f"{basename}: 'spec.source' is missing (ClusterCatalog)"
            )

    elif kind == "UpdateService":
        if not spec.get("graphDataImage", "").strip():
            errors.append(
                f"{basename}: 'spec.graphDataImage' is missing or empty "
                "(UpdateService)"
            )
        if not spec.get("releases", "").strip():
            errors.append(
                f"{basename}: 'spec.releases' is missing or empty "
                "(UpdateService)"
            )

    return errors


manifest_dir = sys.argv[1]
yaml_files = sorted(glob.glob(os.path.join(manifest_dir, "*.yaml")))

if not yaml_files:
    print(f"WARNING: no *.yaml files found in {manifest_dir}", file=sys.stderr)
    sys.exit(0)

all_errors = []
for manifest_path in yaml_files:
    file_errors = validate_manifest(manifest_path)
    for err in file_errors:
        print(f"ERROR: {err}", file=sys.stderr)
    all_errors.extend(file_errors)

if all_errors:
    sys.exit(1)

print(f"OK: all {len(yaml_files)} manifest(s) passed validation.")
PYEOF
