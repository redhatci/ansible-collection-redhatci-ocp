#!/usr/bin/env bash
#
# Copyright (C) 2023, 2024 Red Hat, Inc.
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

HEAD_SHA="$1"
STATUSES_URL="https://api.github.com/repos/redhatci/ansible-collection-redhatci-ocp/statuses/$HEAD_SHA"
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

set -x

# Lookup the merge commits and get their PR descriptions to detect Test-Hints: strings
COMMIT=HEAD
VIRT=
while true; do
    PR=$(git log -1 "$COMMIT" --|grep -oP 'Merge pull request #\K\d+')
    if [ -n "$PR" ]; then
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
    else
        break
    fi
    COMMIT="${COMMIT}^"
done

# if nothing is specified
if [ -z "$VIRT" ]; then
    VIRT=--virt
fi

# copy the change to another directory to let test-runner manage it
DIR=$HOME/github/ansible-collection-redhatci-ocp-mq-$HEAD_SHA
mkdir -p "$DIR"
cp -a "$PWD/" "$DIR/"
CLCTDIR=$DIR/ansible-collection-redhatci-ocp

cd "$DIR" || exit 1

export DCI_SILENT=1
# shellcheck disable=SC2086
dci-queue schedule "$DCI_QUEUE" -- env GITHUB_TOKEN=$GITHUB_TOKEN STATUSES_URL=$STATUSES_URL DCI_SILENT=$DCI_SILENT UPGRADE_ARGS="$UPGRADE_ARGS" APP_NAME=$APP_NAME APP_ARGS="$APP_ARGS" $CLCTDIR/hack/test-runner-wrapper $VIRT $FORCE_CHECK $TAG $UPGRADE $NO_COMMENT $DIR -p @RESOURCE $OPTS

# dci-merge.sh ends here
