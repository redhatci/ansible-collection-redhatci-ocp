#!/bin/bash
#
# Verify that all FQCN module references in task files resolve to
# real, loadable Ansible modules. ansible-lint only checks format,
# not existence — this script catches wrong collection namespaces
# (e.g. ansible.builtin.sefcontext instead of community.general.sefcontext).
#
# Usage: ./hack/check_fqcn_modules.sh [path...]
#   Defaults to scanning roles/ if no path is given.

set -euo pipefail

SCAN_PATHS=("${@:-roles/}")

# Extract FQCN module names from task files.
# Matches lines like "  ansible.builtin.copy:" or "  community.general.nmcli:"
# Extracts only the dotted module name, stripping any value after the colon.
modules=$(
    grep -roh --include='*.yml' --include='*.yaml' \
        -E '^\s+[a-z_]+\.[a-z_]+\.[a-z_]+:' "${SCAN_PATHS[@]}" |
    sed -E 's/^\s+//; s/:$//' |
    grep -v '^\s*#' |
    sort -u
)

if [ -z "$modules" ]; then
    echo "No FQCN module references found."
    exit 0
fi

total=0
failed=0
failures=()

for mod in $modules; do
    total=$((total + 1))
    if ! ansible-doc "$mod" > /dev/null 2>&1; then
        failed=$((failed + 1))
        failures+=("$mod")
    fi
done

echo "Checked $total unique FQCN modules."

if [ "$failed" -gt 0 ]; then
    echo ""
    echo "ERROR: $failed module(s) could not be resolved:"
    for f in "${failures[@]}"; do
        # Show where it's used
        locations=$(grep -rl --include='*.yml' --include='*.yaml' \
            "  ${f}:" "${SCAN_PATHS[@]}" 2>/dev/null | head -5)
        echo "  - $f"
        for loc in $locations; do
            echo "      used in: $loc"
        done
    done
    exit 1
else
    echo "All modules resolved successfully."
fi
