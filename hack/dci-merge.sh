#!/usr/bin/env bash
#
# Copyright (C) 2023-2024 Red Hat, Inc.
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

# script called from a merge queue branch of the redhatci/ansible-collection-redhatci-ocp repo

if [ $# -ne 2 ]; then
    echo "Usage: $0 <base_sha> <head_sha>"
    exit 1
fi

BASE_SHA="$1"
HEAD_SHA="$2"
STATUSES_URL="https://api.github.com/repos/redhatci/ansible-collection-redhatci-ocp/statuses/$HEAD_SHA"
GITHUB_JOBNAME="DCI / DCI Job"
DCI_QUEUE=
FORCE_CHECK=

# shellcheck disable=SC1091
if [ -r /etc/dci-openshift-agent/config ]; then
    . /etc/dci-openshift-agent/config
fi

GH_HEADERS=(
    "Accept: application/vnd.github.v3+json"
    "Authorization: token ${GITHUB_TOKEN}"
)

send_status() {
    curl -s "${GH_HEADERS[@]/#/-H}" -X POST -d "{\"state\":\"$1\",\"description\":\"$2\",\"context\":\"$GITHUB_JOBNAME\"}" "$STATUSES_URL"
}

set -x

# Lookup the merge commits and get their PR descriptions to detect Test-Hints: strings
PRS="$(git log --merges "${BASE_SHA}".."${HEAD_SHA}" | grep -oP 'Merge pull request #\K\d+')"

NB_PRS=0
NB_NOCHECK=0
# CMD is a list of commands to run for each PR
declare -a CMD
declare -a CMD_SNO
declare -a CMD_SNO_BM

for PR in $PRS; do
    if [ -n "$PR" ]; then
        NB_PRS=$((NB_PRS+1))
        DESC=$(curl -s "${GH_HEADERS[@]/#/-H}" https://api.github.com/repos/redhatci/ansible-collection-redhatci-ocp/pulls/"$PR"|jq -r .body)

        if [[ no-check =~ $SUPPORTED_HINTS ]] && grep -qEi "^\s*Test-Hints?:\s*no-check\s*" <<< "$DESC"; then
            NB_NOCHECK=$((NB_NOCHECK+1))
            continue
        fi

        if [[ force-check =~ $SUPPORTED_HINTS ]] && grep -qEi "^\s*Test-Hints?:\s*force-check\s*" <<< "$DESC"; then
            FORCE_CHECK=1
        fi

        # extract TestBos2 commands
        if grep -qE "^\s*TestBos2:\s*" <<< "$DESC"; then
            # shellcheck disable=SC2001,SC2086
            CMD+=("$(sed -ne 's/^\s*TestBos2:\s*//p' <<< $DESC)")
        fi
        # extract TestBos2Sno commands
        if grep -qE "^\s*TestBos2Sno:\s*" <<< "$DESC"; then
            # shellcheck disable=SC2001,SC2086
            CMD_SNO+=("$(sed -ne 's/^\s*TestBos2Sno:\s*//p' <<< $DESC)")
        fi
        # extract TestBos2Baremetal commands
        if grep -qE "^\s*TestBos2Baremetal:\s*" <<< "$DESC"; then
            # shellcheck disable=SC2001,SC2086
            CMD_SNO_BM+=("$(sed -ne 's/^\s*TestBos2Baremetal:\s*//p' <<< $DESC)")
        fi
    fi
done

# Check if there is a code change
if [ -z "$FORCE_CHECK" ] && ! git diff --name-only "$BASE_SHA" "$HEAD_SHA" | grep -v '\.md$' | grep -E 'roles/|plugins/'; then
    send_status success "No code change"
    exit 0
fi


# if nothing is specified
if [ -z "$FORCE_CHECK" ]; then
    if [ "$NB_NOCHECK" -ge 1 ] && [ "$NB_NOCHECK" -eq "$NB_PRS" ]; then
        send_status success "No check"
        exit 0
    fi
fi

# Copy the change to another directory to let test-runner own
# it. Avoid the directory being removed by the Github action code.
DIR=$HOME/github/ansible-collection-redhatci-ocp-mq-$HEAD_SHA
mkdir -p "$DIR"
cp -a "$PWD/" "$DIR/"

cd "$DIR" || exit 1

# Create a json file to be used by send-feedback and test-runner
cat > github.json << EOF
{
    "number": "${HEAD_SHA:0:8}",
    "url": "https://github.com/redhatci/ansible-collection-redhatci-ocp/pulls",
    "statuses_url": "$STATUSES_URL",
    "html_url": "https://github.com/redhatci/ansible-collection-redhatci-ocp/queue/main",
    "body": "",
    "head": {
        "repo": {
            "full_name": "redhatci/ansible-collection-redhatci-ocp",
            "name": "ansible-collection-redhatci-ocp"
        }
    }
}
EOF

COUNT=0

for ARGS in "${CMD[@]}"; do
    # shellcheck disable=SC2086
    dci-queue schedule "$DCI_QUEUE" -- env GITHUB_TOKEN=$GITHUB_TOKEN STATUSES_URL=$STATUSES_URL DCI_QUEUE_RESOURCE=@RESOURCE /usr/share/dci-pipeline/test-runner $DIR $ARGS || exit 1
    COUNT=$((COUNT+1))
done

dci-queue list "$DCI_QUEUE"

if [ ${#CMD_SNO[@]} -gt 0 ]; then
    DCI_QUEUE="sno"

    for ARGS in "${CMD_SNO[@]}"; do
        # shellcheck disable=SC2086
        dci-queue schedule "$DCI_QUEUE" -- env GITHUB_TOKEN=$GITHUB_TOKEN STATUSES_URL=$STATUSES_URL DCI_QUEUE_RESOURCE=@RESOURCE /usr/share/dci-pipeline/test-runner $DIR $ARGS || exit 1
        COUNT=$((COUNT+1))
    done

    dci-queue list "$DCI_QUEUE"
fi

if [ ${#CMD_SNO_BM[@]} -gt 0 ]; then
    DCI_QUEUE="sno_baremetal"

    for ARGS in "${CMD_SNO_BM[@]}"; do
        # shellcheck disable=SC2086
        dci-queue schedule "$DCI_QUEUE" -- env GITHUB_TOKEN=$GITHUB_TOKEN STATUSES_URL=$STATUSES_URL DCI_QUEUE_RESOURCE=@RESOURCE /usr/share/dci-pipeline/test-runner $DIR $ARGS || exit 1
        COUNT=$((COUNT+1))
    done

    dci-queue list "$DCI_QUEUE"
fi

if [ $COUNT -eq 0 ]; then
    send_status success "No test specified for BOS2"
    exit 0
fi

send_status pending "QUEUED"

# dci-merge.sh ends here
