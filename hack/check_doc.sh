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

# when run outside of a GitHub action
if [ -z "$GITHUB_STEP_SUMMARY" ]; then
    GITHUB_STEP_SUMMARY=/dev/null
fi

rc=0

echo "# Missing roles in README" >> ${GITHUB_STEP_SUMMARY}
while read -r role_readme; do
  role="${role_readme%/*}"  # strip last file `/README.md``
  role="${role#*/}"         # strip left `roles/`
  role="${role/\//.}"       # replace `/` with `.`
  if ! grep -q "^\[redhatci\.ocp\.${role}\]" README.md; then
    echo "- Missing: ${role}" | tee -a ${GITHUB_STEP_SUMMARY}
    rc=1
  fi
done < <(find roles -name README.md)

echo "# Additional roles/plugins in README" >> ${GITHUB_STEP_SUMMARY}
while read -r role; do
  rp="${role/redhatci.ocp./}"
  if [[ ! -d "roles/${rp/./\/}" ]] &&
     [[ ! -r "plugins/filter/${rp}.py" ]] &&
     [[ ! -r "plugins/modules/${rp}.py" ]]; then
    echo "- Extra role/plugin found in README: ${role}" | tee -a ${GITHUB_STEP_SUMMARY}
    rc=1
  fi
done < <(grep -Po '^\[redhatci\.ocp\.[^\]]+' README.md | tr -d '[')

exit $rc

# check_doc.sh ends here
