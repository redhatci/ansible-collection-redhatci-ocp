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

RUN_IN_PARALLEL="${RUN_IN_PARALLEL:-0}"

# Mac compatibility: use gnu utils if available
GREP="grep"
SED="sed"
if [[ "$(uname -s || true)" == "Darwin" ]]; then
  if command -v ggrep >/dev/null 2>&1; then
    GREP="ggrep"
  fi
  if command -v gsed >/dev/null 2>&1; then
    SED="gsed"
  fi
fi

# when run outside of a GitHub action
if [ -z "$GITHUB_STEP_SUMMARY" ]; then
    GITHUB_STEP_SUMMARY=/dev/null
    > branch.output
    > main.output
fi

branch=$(git rev-parse --abbrev-ref HEAD)

trap 'git checkout "$branch"' EXIT

# Parse test types from arguments, default to all
TEST_TYPES=()
if [[ $# -eq 0 ]]; then
  TEST_TYPES=(
    sanity
    units
    integration
  )
else
  for arg in "$@"; do
    case "${arg}" in
      sanity|units|integration)
        TEST_TYPES+=("${arg}")
        ;;
      *)
        echo "Unknown test type: ${arg}"
        echo "Usage: $0 [sanity] [units] [integration]"
        exit 2
        ;;
    esac
  done
fi
declare -a TEST_PIDS
run_tests() {
  local \
    version \
    prefix
  local -a \
    cmd
  version="${1?cannot have version empty}"
  prefix="${2?cannot have prefix empty}"
  for test_type in "${TEST_TYPES[@]}"; do
    case "$test_type" in
      sanity)
        cmd=(ansible-test "${test_type}" $EXCLUDE --verbose --docker --python ${version} --color \
        --coverage --failure-ok --lint)
        ;;
      units)
        cmd=(ansible-test units --verbose --docker --python ${version} --color --coverage)
        ;;
      integration)
        cmd=(ansible-test integration --verbose --docker --python ${version} --color --coverage)
        ;;
    esac
    if [[ "${RUN_IN_PARALLEL}" -gt 0 ]]; then
      ("${cmd[@]}" \
        2>&1 > "${prefix}.${test_type}.${version}.output" || true) &
      TEST_PIDS+=($!)
      echo "Running ${test_type} tests for ${version} in parallel"
    else
      "${cmd[@]}" \
        2>&1  || true
    fi
  done
}

# extract all the supported python versions from the error message, excluding 3.5
EXCLUDE="--exclude tests/ --exclude hack/ --exclude plugins/modules/nmcli.py"
PY_VERS=$(ansible-test sanity $EXCLUDE --verbose --docker --python 1.0 --color --coverage --failure-ok 2>&1 |
  grep -Po "invalid.*?\K'3.*\d'" |
  tr -d ,\' |
  sed -e 's/3.5 //g')

# Tests in current branch
for version in $PY_VERS; do
  run_tests "${version}" "branch"
done 2> >(tee -a branch.output >&2)

# Tests in main branch
git fetch origin main
git checkout main
echo "Running tests in main branch, this may take a while as no output is displayed..."
for version in $PY_VERS; do
  run_tests "${version}" "main"
done 2> main.output 1>/dev/null

if [[ "${RUN_IN_PARALLEL}" -gt 0 ]]; then
  echo "Waiting for tests to complete..."
  wait "${TEST_PIDS[@]}"
fi

for key in branch main; do
  "${GREP}" -E "((ERROR|FATAL):|FAILED )" "${key}.*.output" |
  "${GREP}" -v "issue(s) which need to be resolved\|See error output above for details.\|Command \"ansible-doc -t module .*\" returned exit status .*\." |
  "${SED}" -r 's/\x1B\[[0-9]{1,2}[mGK]//g' > "${key}.errors"
done

# remove line numbers
"${SED}" -i -E -e 's/:[0-9]+:/:/' -e 's/:[0-9]+:/:/' branch.errors main.errors
set +ex
echo "## Improvements are listed below" | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`diff" >> ${GITHUB_STEP_SUMMARY}
diff -u0 branch.errors main.errors | "${GREP}" '^+[^+]' | "${SED}" -e 's/ERROR/FIXED/' | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`" >> ${GITHUB_STEP_SUMMARY}
echo "## Regressions are listed below" | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`diff" >> ${GITHUB_STEP_SUMMARY}
diff -u0 branch.errors main.errors | "${GREP}" '^-[^-]' | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`" >> ${GITHUB_STEP_SUMMARY}

if diff -u0 branch.errors main.errors | "${GREP}" -q '^-[^-]'; then
   echo "> Fix the regression errors listed above" | tee -a ${GITHUB_STEP_SUMMARY}
   exit 1
fi

# run_ansible_test.sh ends here
