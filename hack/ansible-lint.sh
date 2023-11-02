#!/bin/bash -x
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
#~  -f          Force linting of all roles
#~  -p PROFILE  (default: shared) What ansible lint profile to use

function usage(){
    grep '^#~' $0 | sed -e 's/#~//'
}

TOPDIR="$(git rev-parse --show-toplevel)"
CWD="$PWD"
FORCE=""
PROFILE="shared"

while getopts ":fp" o; do
    case $o in
        f)
            FORCE="yes"
            ;;
        p)
            PROFILE="production"
            ;;
        *)
            usage
            ;;
    esac
done

cd $TOPDIR

for role in roles/*; do
    clear
    echo $role
    if [ "$FORCE" != "yes" ] && [ -f $role/.linted ]; then
        continue
    else
        ansible-lint --profile="$PROFILE" $role && touch $role/.linted || break
    fi
done

cd $CWD
