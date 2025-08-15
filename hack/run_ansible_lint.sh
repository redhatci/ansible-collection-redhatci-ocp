#!/usr/bin/env bash
# Run ansible-lint on this branch then compare vs main branch
set +e
SCRIPT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
# Source the library file using the absolute path
source "${SCRIPT_DIR}/base.bash"
set -x
# fix randomness
export PYTHONHASHSEED=42
git checkout -b branch
git fetch --unshallow origin main || :
cmd="hack/ansible-lint.sh -d"
# don't want to annotate through GHA
unset GITHUB_ACTIONS
# To leave the workspace as it was before, it is better to setup the trap on EXIT:
current_branch="$(git rev-parse --abbrev-ref HEAD || true)"
trap "git checkout '${current_branch}'" EXIT

echo "=== Incoming branch ==="
$cmd | tee branch.output
git checkout main
echo "=== Main branch ==="
$cmd | tee main.output
export GITHUB_ACTIONS=true
set +ex
# remove line numbers
"${SED}" -i -r 's/:[0-9]+:/::/' branch.output main.output
# export diff sans headers
diff -u0 branch.output main.output | tail -n +3 > diff.raw
# Get warnings out of the diff
"${GREP}" -P '\x1B\[33m|\(warning\)(\x1B\[0m)?$' diff.raw > diff.warnings
"${GREP}" -vP '\x1B\[33m|\(warning\)(\x1B\[0m)?$' diff.raw > diff.output
echo "## Improvements over main branch:" | tee -a ${GITHUB_STEP_SUMMARY}
echo '```diff' >> ${GITHUB_STEP_SUMMARY}
"${GREP}" '^+' diff.output |
  "${SED}" -e 's/^+/+FIXED: /' |
  "${SED}" -r 's/\x1B\[[0-9]{1,2}(;[0-9]{1,2})?[mGK]//g' |
  tee -a ${GITHUB_STEP_SUMMARY}
echo '```' >> ${GITHUB_STEP_SUMMARY}
echo "## Regressions from main branch:" | tee -a ${GITHUB_STEP_SUMMARY}
echo '```diff' >> ${GITHUB_STEP_SUMMARY}
"${GREP}" '^-' diff.output |
  "${SED}" -e 's/^-/-ERROR: /' |
  "${SED}" -r 's/\x1B\[[0-9]{1,2}(;[0-9]{1,2})?[mGK]//g' |
  tee -a ${GITHUB_STEP_SUMMARY}
echo '```' >> ${GITHUB_STEP_SUMMARY}
echo "## Warnings from main branch:" | tee -a ${GITHUB_STEP_SUMMARY}
echo '```diff' >> ${GITHUB_STEP_SUMMARY}
"${GREP}" '^-' diff.warnings |
  "${SED}" -e 's/^-/-WARNING: /' |
  "${SED}" -r 's/\x1B\[[0-9]{1,2}(;[0-9]{1,2})?[mGK]//g' |
  tee -a ${GITHUB_STEP_SUMMARY}
echo '```' >> ${GITHUB_STEP_SUMMARY}
if "${GREP}" -q '^-' diff.output; then
   echo "> Fix regressions listed above" | tee -a ${GITHUB_STEP_SUMMARY}
   exit 1
fi
