#!/bin/bash
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

# when run outside of a GitHub action
LOCAL_RUN=
if [ -z "$GITHUB_STEP_SUMMARY" ]; then
    GITHUB_STEP_SUMMARY=/dev/null
    LOCAL_RUN=1
    > branch.output
fi

# Every ansible-test call below uses --docker, mirroring the GitHub Actions
# run. When invoked locally (not in CI), fail fast if there is no usable
# Docker daemon instead of hanging on it. You do NOT need to replicate the
# full CI matrix to reproduce a single CI failure -- run the equivalent
# --local check instead (see AGENTS.md > "Running tests locally").
if [ -n "$LOCAL_RUN" ]; then
    if ! docker info >/dev/null 2>&1 || docker --version 2>/dev/null | grep -qi podman; then
        cat >&2 <<'EOF'
ERROR: run_ansible_test.sh mirrors the GitHub Actions run and needs a real
Docker daemon. None was found, or 'docker' is a Podman symlink (which
ansible-test --docker rejects).

To reproduce a CI failure you do NOT need the full docker matrix. Run the
equivalent check locally, in seconds, e.g.:

    ansible-test sanity --local --requirements plugins/modules/<name>.py

See AGENTS.md > "Running tests locally (without docker)" for details.
EOF
        exit 1
    fi
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

run_tests() {
  local version=$1
  for test_type in "${TEST_TYPES[@]}"; do
    case "$test_type" in
      sanity)
        ansible-test sanity $EXCLUDE --verbose --docker --python ${version} --color --coverage --failure-ok --lint
        ;;
      units)
        ansible-test units --verbose --docker --python ${version} --color --coverage || :
        ;;
      integration)
        ansible-test integration --verbose --docker --python ${version} --color --coverage || :
        ;;
    esac
  done
}

EXCLUDE="--exclude tests/ --exclude hack/ --exclude plugins/modules/nmcli.py"

# Extract the supported python versions (excluding 3.5) from the argparse
# error triggered by an invalid --python value. This is instant and needs no
# docker, so no docker/coverage flags are passed here.
PY_VERS=$(ansible-test sanity --python 1.0 2>&1 |
  grep -Po "invalid.*?\K'3.*\d'" |
  tr -d ,\' |
  sed -e 's/3.5 //g')

# Tests in current branch
for version in $PY_VERS; do
  run_tests "${version}"
done 2> >(tee -a branch.output >&2)

# Tests in main branch. Cache the results by commit SHA so repeated local runs
# (e.g. iterating on a branch) skip re-running the whole main suite when
# origin/main has not moved.
git fetch origin main
main_sha=$(git rev-parse origin/main)
if [ -s main.output ] && [ -f .main.sha ] && [ "$(cat .main.sha)" = "$main_sha" ]; then
  echo "Reusing cached main-branch results for ${main_sha}"
else
  git checkout main
  echo "Running tests in main branch, this may take a while as no output is displayed..."
  for version in $PY_VERS; do
    run_tests "${version}"
  done 2> main.output 1>/dev/null
  echo "$main_sha" > .main.sha
fi

for key in branch main; do
  grep -E "((ERROR|FATAL):|FAILED )" "$key.output" |
  grep -v "issue(s) which need to be resolved\|See error output above for details.\|Command \"ansible-doc -t module .*\" returned exit status .*\." |
  sed -r 's/\x1B\[[0-9]{1,2}[mGK]//g' > "$key.errors"
done

# remove line numbers
sed -i -E -e 's/:[0-9]+:/:/' -e 's/:[0-9]+:/:/' branch.errors main.errors
set +ex
echo "## Improvements are listed below" | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`diff" >> ${GITHUB_STEP_SUMMARY}
diff -u0 branch.errors main.errors | grep '^+[^+]' | sed -e 's/ERROR/FIXED/' | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`" >> ${GITHUB_STEP_SUMMARY}
echo "## Regressions are listed below" | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`diff" >> ${GITHUB_STEP_SUMMARY}
diff -u0 branch.errors main.errors | grep '^-[^-]' | tee -a ${GITHUB_STEP_SUMMARY}
echo "\`\`\`" >> ${GITHUB_STEP_SUMMARY}

if diff -u0 branch.errors main.errors | grep -q '^-[^-]'; then
   echo "> Fix the regression errors listed above" | tee -a ${GITHUB_STEP_SUMMARY}
   exit 1
fi

# run_ansible_test.sh ends here
