#!/bin/bash

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
srpmdir="$(rpm --eval "%{_srcrpmdir}")"
version="$(rpmspec -P ${gittop}/${name}.spec | grep ^Version | tr -s ' ' | cut -d' ' -f 2)"
release="$(rpmspec -P ${gittop}/${name}.spec | grep ^Release | tr -s ' ' | cut -d' ' -f 2)"

branch="main"
mockconfig="centos-stream+epel-8-x86_64"
while getopts ':hb:r:' OPTION; do
    case "$OPTION" in
        b)
            branch="$OPTARG"
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

$(dirname $0)/build-tarball.sh -b ${branch}
$(dirname $0)/build-srpm.sh

set -ex
mock -r "${mockconfig}" --rebuild "${srpmdir}/${name}-${version}-${release}.src.rpm"
