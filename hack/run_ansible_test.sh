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
if [ -z "$GITHUB_STEP_SUMMARY" ]; then
    GITHUB_STEP_SUMMARY=/dev/null
fi

branch=$(git rev-parse --abbrev-ref HEAD)

trap 'git checkout -- "$branch"' EXIT

git fetch --unshallow origin main || :

# extract all the supported python versions from the error message, excluding 3.5
EXCLUDE="--exclude tests/ --exclude hack/ --exclude plugins/modules/nmcli.py"
PY_VERS=$(ansible-test sanity $EXCLUDE --verbose --docker --python 1.0 --color --coverage --failure-ok 2>&1 |
  grep -Po "invalid.*?\K'3.*\d'" |
  tr -d ,\' |
  sed -e 's/3.5 //g')
for version in $PY_VERS; do
  ansible-test sanity $EXCLUDE --verbose --docker --python $version --color --coverage --failure-ok
  ansible-test units --verbose --docker --python $version --color --coverage || :
  ansible-test integration --verbose --docker --python $version --color --coverage || :
done 2> >(tee -a branch.output >&2)
git checkout origin/main
for version in $PY_VERS; do
  ansible-test sanity $EXCLUDE --verbose --docker --python $version --color --coverage --failure-ok
  ansible-test units --verbose --docker --python $version --color --coverage || :
  ansible-test integration --verbose --docker --python $version --color --coverage || :
done 2> main.output 1>/dev/null
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
