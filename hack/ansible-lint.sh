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
#~  ansible-lint.sh [-b BIN] [-d] [PATH]
#~
#~Options:
#~  -b BIN  Path to the `ansible-lint` binary (default: $PATH/ansible-lint)
#~  -d      Download requirements declared in galaxy.yml (default: False)
#~Arguments:
#~  PATH    (Optional) path to lint, defaults to the top level directory

function usage(){
    grep "^#~" "$0" | sed -e "s/#~//"
}

set -x

TOPDIR="$(git rev-parse --show-toplevel)"
CWD="$PWD"
BIN="$(which ansible-lint)"
OFFLINE="--offline"

while getopts ":b:d" o; do
    case $o in
        b)
            BIN="$OPTARG"
            ;;
        d)
            OFFLINE=""
            ;;
        *)
            usage
            exit
            ;;
    esac
done

shift $((OPTIND-1))
EXTRA_ARGS="$@"

if ! test -x $BIN; then
    echo "You need to install ansible-lint. Ideally from the source code branch"
    echo "Example:"
    echo -e "pip install 'ansible-lint[lock] @ git+https://github.com/ansible/ansible-lint@v6'"
    exit 1
fi

cd "$TOPDIR"

$BIN \
    $OFFLINE \
    --force-color \
    --parseable \
    $EXTRA_ARGS

cd "$CWD"
