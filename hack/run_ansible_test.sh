#!/usr/bin/env bash
#
# Copyright (C) 2025 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

set -ex

REQS_DEFAULT="meta/requirements.txt"
PY_VERS_EXCL="${PY_VERS_EXCL:-"3.5"}"
declare -a TEST_TYPES_DEFAULT
declare -a TEST_TYPES
declare -a EXCLUDE_ITEMS
declare -a EXCLUDES
declare -a PY_VERSIONS

TEST_TYPES_DEFAULT=(
  "sanity"
  "units"
  "integration"
)
EXCLUDE_ITEMS=(
  "tests/"
  "hack/"
  "plugins/modules/nmcli.py"
)
for exclude in "${EXCLUDE_ITEMS[@]}"; do
  EXCLUDES+=("--exclude" "${exclude}")
done
GREP="grep"
SED="sed"
if [[ "$(uname -s || true)" == "Darwin" ]]; then
  GREP="ggrep"
  SED="gsed"
fi
# when run outside of a GitHub action
if [[ -z "${GITHUB_STEP_SUMMARY}" ]]; then
  GITHUB_STEP_SUMMARY=/dev/null
  echo "" >branch.output || true
  echo "" >main.output || true
fi

usage() {
  echo "Usage: $0$(for tt in "${TEST_TYPES_DEFAULT[@]}"; do echo -n " [${tt}]"; done)"
}

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [[ -n "${branch}" ]]; then
  trap 'git checkout "${branch}"' EXIT
fi

# Parse test types from arguments, default to all
TEST_TYPES=()
if [[ $# -eq 0 ]]; then
  TEST_TYPES=("${TEST_TYPES_DEFAULT[@]}")
else
  for arg in "${@}"; do
    case "${arg}" in
    sanity | units | integration)
      TEST_TYPES+=("${arg}")
      ;;
    *)
      echo "Unknown test type: ${arg}" >&2
      usage
      exit 2
      ;;
    esac
  done
fi

function run_tests() {
  local version="${1?cannot run_tests() without version}"
  local reqs="${2:-"${REQS_DEFAULT}"}"
  local -a cmd_parts=(
    --verbose
    --docker
    --python "${version}"
    --color
    --coverage
    --requirements "${reqs}"
  )
  for test_type in "${TEST_TYPES[@]}"; do
    case "${test_type}" in
    sanity)
      ansible-test sanity "${cmd_parts[@]}" "${EXCLUDES[@]}" --failure-ok --lint
      ;;
    units)
      ansible-test units "${cmd_parts[@]}" || true
      ;;
    integration)
      ansible-test integration "${cmd_parts[@]}" || true
      ;;
    *)
      echo "Unknown test type: ${test_type}" >&2
      usage
      exit 2
      ;;
    esac
  done
}

# extract all the supported python versions from the error message, excluding 3.5
mapfile -t PY_VERSIONS < <(
  ansible-test sanity "${EXCLUDES[@]}" --docker --python 1.0 --failure-ok 2>&1 |
    python -c "import re, sys; print('\n'.join({m.group(1) for m in re.finditer(r'(3\.\d+)', sys.stdin.read()) if m.group(1) != '${PY_VERS_EXCL}'}))" || true
)

# Tests in current branch
echo "Running tests in current branch: ${branch}, this may take a while as no output is displayed ..."
for version in "${PY_VERSIONS[@]}"; do
  run_tests "${version}"
done 2> >(tee -a branch.output >&2 || true)

# Tests in main branch
git fetch origin main
git checkout main
echo "Running tests in main branch, this may take a while as no output is displayed ..."
for version in "${PY_VERSIONS[@]}"; do
  run_tests "${version}"
done 2>main.output 1>/dev/null

for key in branch main; do
  "${GREP}" -E "((ERROR|FATAL):|FAILED )" "${key}.output" |
    "${GREP}" -v "issue(s) which need to be resolved\|See error output above for details.\|Command \"ansible-doc -t module .*\" returned exit status .*\." |
    "${SED}" -r 's/\x1B\[[0-9]{1,2}[mGK]//g' >"${key}.errors" || true
done

# remove line numbers
"${SED}" -i -E -e 's/:[0-9]+:/:/' -e 's/:[0-9]+:/:/' branch.errors main.errors
set +ex
echo "## Improvements are listed below" | tee -a "${GITHUB_STEP_SUMMARY}"
echo "\`\`\`diff" >>"${GITHUB_STEP_SUMMARY}"
diff -u0 branch.errors main.errors | "${GREP}" '^+[^+]' | "${SED}" -e 's/ERROR/FIXED/' | tee -a "${GITHUB_STEP_SUMMARY}" || true
echo "\`\`\`" >>"${GITHUB_STEP_SUMMARY}"
echo "## Regressions are listed below" | tee -a "${GITHUB_STEP_SUMMARY}"
echo "\`\`\`diff" >>"${GITHUB_STEP_SUMMARY}"
diff -u0 branch.errors main.errors | "${GREP}" '^-[^-]' | tee -a "${GITHUB_STEP_SUMMARY}" || true
echo "\`\`\`" >>"${GITHUB_STEP_SUMMARY}"

if (diff -u0 branch.errors main.errors || true) | "${GREP}" -q '^-[^-]'; then
  echo "> Fix the regression errors listed above" | tee -a "${GITHUB_STEP_SUMMARY}"
  exit 1
fi

# run_ansible_test.sh ends here
