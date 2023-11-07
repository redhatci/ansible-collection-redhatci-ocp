#!/usr/bin/env bash
#
# Copyright (C) 2023 Red Hat, Inc.
#
# Author: Jorge A Gallegos <jgallego@redhat.com>
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
#
#~Usage:
#~  ansible-lint.sh [-f] [-p PROFILE]
#~
#~Options:
#~  -c      Remove .linted markers
#~  -p      Use the "production" ansible-lint profile
#~  -n      Don't clear screen after linting each role

function usage(){
    grep "^#~" "$0" | sed -e "s/#~//"
}

TOPDIR="$(git rev-parse --show-toplevel)"
CWD="$PWD"
CLEAN=""
PROFILE="shared"
CLEAR="yes"

while getopts ":cpn" o; do
    case $o in
        c)
            CLEAN="yes"
            ;;
        p)
            PROFILE="production"
            ;;
        n)
            CLEAR=""
            ;;
        *)
            usage
            exit
            ;;
    esac
done

# Be verbose from this point forward
set -x

cd "$TOPDIR"

if [ "$CLEAN" == "yes" ]; then
    rm -fv roles/*/.linted
fi

for role in roles/*; do
    if [ "$CLEAR" == "yes" ]; then
        clear
    fi
    echo "$role"
    if [ -f "$role/.linted" ]; then
        continue
    else
        if ansible-lint --profile="$PROFILE" "$role"; then
            touch "$role/.linted"
        else
            break
        fi
    fi
done

cd "$CWD"
