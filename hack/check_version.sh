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

# Usage: check_version.sh
#
# Implement 2 checks:
# 1. check that the version numbers in galaxy.yml and rpm spec file are consistent
#
# 2. check major and minor version management according to our policy:
# - If there is a removed role, check that the major version is incremented.
# - If there is a new role, check that the minor version is incremented.

error() {
    if [ -n "${GITHUB_STEP_SUMMARY}" ]; then
        echo "- check_version: ${1}" | tee -a "${GITHUB_STEP_SUMMARY}"
    else
        echo "Error: check_version: ${1}"
    fi
    exit 1
}

# Verify consistency of version numbers in galaxy.yml and rpm spec file
spec_version=$(grep Version: ansible-collection-redhatci-ocp.spec | awk '{print $2}' | cut -d. -f1,2)
galaxy_version=$(grep version: galaxy.yml | awk '{print $2}' | cut -d. -f1,2)

if [ "$spec_version" != "$galaxy_version" ]; then
    error "Inconsistent: rpm spec: ${spec_version} galaxy: ${galaxy_version}"
fi

branch=$(git rev-parse --abbrev-ref HEAD)

if [ -z "$branch" ]; then
    error "Unable to determine the current branch."
fi

EXISTING=$(git ls-tree -r --name-only origin/main |
  grep -E '^roles/.+/' |
  sed -E -e 's@^roles/@@' -e 's@/(defaults|templates|vars|scripts|handlers|tests|meta|tasks|files).*@@' -e 's@/.*@@' |
  uniq)

ADDED_FILES=$(git diff --diff-filter=A --name-only origin/main...$branch)

REMOVED_FILES=$(git diff --diff-filter=D --name-only origin/main...$branch)

ADDED=$(echo "$ADDED_FILES" |
  grep -E '^roles/.+/' |
  sed -E -e 's@^roles/@@' -e 's@/(defaults|templates|vars|scripts|handlers|tests|meta|tasks|files).*@@' -e 's@/.*@@' |
  uniq)

REMOVED=$(echo "$REMOVED_FILES" |
  grep -E '^roles/.+/' |
  sed -E -e 's@^roles/@@' -e 's@/(defaults|templates|vars|scripts|handlers|tests|meta|tasks|files).*@@' -e 's@/.*@@' |
  uniq)

NEW=$(comm -23 <(echo "$ADDED" | sort) <(echo "$EXISTING_ROLES" | sort))

DELETED=$(comm -23 <(echo "$EXISTING" | sort) <(echo "$REMOVED" | sort))

# check if the roles are fully removed
if [ -n "$DELETED" ]; then
    for role in $DELETED; do
        if [ ! -d "roles/$role" ]; then
            # role is fully removed, so check if the major version is
            # incremented in galaxy.yml
            major=$(grep -E '^version:' galaxy.yml | awk '{print $2}' | cut -d'.' -f1)
            # get the major version from the main branch
            major_main=$(git show origin/main:galaxy.yml | grep -E '^version:' | awk '{print $2}' | cut -d'.' -f1)
            # check if the major version is incremented
            if [ "$major" -le "$major_main" ]; then
                error "Major version must be incremented for removed role $role"
            fi
        fi
    done
fi

# check if the roles are fully added
if [ -n "$NEW" ]; then
    for role in $NEW; do
        # check if $role doesn't exist in the main branch
        if ! git show origin/main:roles/$role > /dev/null 2>&1; then
            # role is fully added, so check if the minor version is
            # incremented in galaxy.yml. Check major and minor version
            # in the case there was a removed role.
            major=$(grep -E '^version:' galaxy.yml | awk '{print $2}' | cut -d'.' -f1)
            minor=$(grep -E '^version:' galaxy.yml | awk '{print $2}' | cut -d'.' -f2)
            # get the minor version from the main branch
            major_main=$(git show origin/main:galaxy.yml | grep -E '^version:' | awk '{print $2}' | cut -d'.' -f1)
            minor_main=$(git show origin/main:galaxy.yml | grep -E '^version:' | awk '{print $2}' | cut -d'.' -f2)
            # check if major.minor is greater than the main branch
            if [ "$major" -lt "$major_main" ]; then
                error "Minor version (${major}.${minor}) must be incremented for new role ${role}"
            elif [ "$major" -eq "$major_main" ]; then
                if [ "$minor" -le "$minor_main" ]; then
                    error "Minor version ${minor} must be incremented for new role ${role}"
                fi
            fi
        fi
    done
fi

# check_version.sh ends here
