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
VIRT=
DCI_QUEUE=
SNO_DCI_QUEUE=
SUPPORTED_HINTS=
NO_DCI_QUEUE=${NO_DCI_QUEUE:-}
NO_COMMENT=
UPGRADE=
UPGRADE_ARGS=
APP_NAME=
APP_ARGS=
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

# Check if there is a code change
if ! git diff --name-only "$BASE_SHA" "$HEAD_SHA" | grep -v '\.md$' | grep -E 'roles/|plugins/'; then
    send_status success "No code change"
    exit 0
fi

# Lookup the merge commits and get their PR descriptions to detect Test-Hints: strings
VIRT=
PRS=$(git log --merges ${BASE_SHA}..${HEAD_SHA} | grep -oP 'Merge pull request #\K\d+')

NB_PRS=0
NB_NOCHECK=0
for PR in $PRS; do
    if [ -n "$PR" ]; then
        NB_PRS=$((NB_PRS+1))
        DESC=$(curl -s "${GH_HEADERS[@]/#/-H}" https://api.github.com/repos/redhatci/ansible-collection-redhatci-ocp/pulls/"$PR"|jq -r .body)

        if [[ sno =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*sno\s*" <<< "$DESC"; then
            VIRT=--sno
            if [ -n "$SNO_DCI_QUEUE" ]; then
                DCI_QUEUE="$SNO_DCI_QUEUE"
            fi
        fi

        if [[ sno-ai =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*sno-ai\s*" <<< "$DESC"; then
            VIRT=--sno-ai
            if [ -n "$SNO_AI_DCI_QUEUE" ]; then
                DCI_QUEUE="$SNO_AI_DCI_QUEUE"
            fi
        fi

        if [[ assisted =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*assisted\s*" <<< "$DESC"; then
            VIRT=--assisted
            if [ -n "$ASSISTED_DCI_QUEUE" ]; then
                DCI_QUEUE="$ASSISTED_DCI_QUEUE"
            fi
        fi

        if [[ assisted-abi =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*assisted-abi\s*" <<< "$DESC"; then
            VIRT=--assisted-abi
            if [ -n "$ASSISTED_DCI_QUEUE" ]; then
                DCI_QUEUE="$ASSISTED_DCI_QUEUE"
            fi
        fi

        if [[ libvirt =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*libvirt\s*" <<< "$DESC"; then
            VIRT=--virt
        fi

        if [[ no-check =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*no-check\s*" <<< "$DESC"; then
            NB_NOCHECK=$((NB_NOCHECK+1))
            continue
        fi

        if [[ force-check =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Hints:\s*force-check\s*" <<< "$DESC"; then
            FORCE_CHECK=--force-check
        fi

        if [[ upgrade =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Upgrade-Hints:\s*yes\s*" <<< "$DESC"; then
            UPGRADE=--upgrade
        
            if [ -z "$VIRT" ]; then
                VIRT=--virt
            fi

            # process Test-Upgrade-Args-Hints
            if [[ upgrade-args =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Upgrade-Args-Hints:" <<< "$DESC"; then
                UPGRADE_ARGS="$(sed -n -e 's/^\s*Test-Upgrade-Args-Hints:\s*//pi' <<< "$DESC")"
            fi

            # process Test-Upgrade-From-Topic-Hints
            if [[ upgrade-from-topic =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Upgrade-From-Topic-Hints:" <<< "$DESC"; then
                UPGRADE="$UPGRADE --from-topic $(sed -n -e 's/^\s*Test-Upgrade-From-Topic-Hints:\s*//pi' <<< "$DESC")"
            fi

            # process Test-Upgrade-To-Topic-Hints
            if [[ upgrade-to-topic =~ $SUPPORTED_HINTS ]] && grep -qi "^\s*Test-Upgrade-To-Topic-Hints:" <<< "$DESC"; then
                UPGRADE="$UPGRADE --to-topic $(sed -n -e 's/^\s*Test-Upgrade-To-Topic-Hints:\s*//pi' <<< "$DESC")"
            fi
        fi

        if [ -n "$VIRT" ]; then
            # process Test-Args-Hints
            if [[ args =~ $SUPPORTED_HINTS ]]; then
                OPTS=$(sed -n -e "s/^\s*Test-Args-Hints:\s*//pi" <<< "$DESC")
            else
                OPTS=
            fi

            # process Test-App-Hints
            if [[ app =~ $SUPPORTED_HINTS ]]; then
                APP_NAME=$(sed -n -e "s/^\s*Test-App-Hints:\s*//pi" <<< "$DESC")
            fi

            # process Test-App-Args-Hints
            if [[ app-args =~ $SUPPORTED_HINTS ]]; then
                APP_ARGS=$(sed -n -e "s/^\s*Test-App-Args-Hints:\s*//pi" <<< "$DESC")
            fi

            # stop at the first valid Test-Hints: string
            break
        fi
    fi
done

# if nothing is specified
if [ -z "$VIRT" ]; then
    if [ "$NB_NOCHECK" -eq "$NB_PRS" ]; then
        send_status success "No check"
        exit 0
    fi
    VIRT=--sno
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
    "head": {
        "repo": {
            "full_name": "redhatci/ansible-collection-redhatci-ocp",
            "name": "ansible-collection-redhatci-ocp"
        }
    }
}
EOF

# shellcheck disable=SC2086
dci-queue schedule "$DCI_QUEUE" -- env GITHUB_TOKEN=$GITHUB_TOKEN STATUSES_URL=$STATUSES_URL UPGRADE_ARGS="$UPGRADE_ARGS" APP_NAME=$APP_NAME APP_ARGS="$APP_ARGS" /usr/share/dci-openshift-agent/test-runner $VIRT $FORCE_CHECK $TAG $UPGRADE $NO_COMMENT $DIR -p @RESOURCE $OPTS || exit 1

send_status pending "QUEUED"

dci-queue list "$DCI_QUEUE"

# dci-merge.sh ends here
