#!/bin/bash

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
srpmdir="$(rpm --eval "%{_srcrpmdir}")"
version="$(rpmspec -P ${gittop}/${name}.spec | grep ^Version | tr -s ' ' | cut -d' ' -f 2)"
release="$(rpmspec -P ${gittop}/${name}.spec | grep ^Release | tr -s ' ' | cut -d' ' -f 2)"

branch=""
mockconfig="centos-stream+epel-8-x86_64"
while getopts ':hb:r:' OPTION; do
    case "$OPTION" in
        b)
            branch="-b $OPTARG"
            ;;
        r)
            mockconfig="$OPTARG"
            ;;
        h)
            echo "Usage: $(basename $0) [-d] [-b BRANCH] [-r MOCKCONFIG]"
            exit 0
            ;;
        ?)
            echo "Usage: $(basename $0) [-d] [-b BRANCH] [-r MOCKCONFIG]"
            exit 1
    esac
done

set -ex

$(dirname $0)/build-tarball.sh ${branch}
$(dirname $0)/build-srpm.sh

mock -r "${mockconfig}" --rebuild "${srpmdir}/${name}-${version}-${release}.src.rpm"
