#!/bin/bash

dirty=true
branch="main"
while getopts ':hb:' OPTION; do
    case "$OPTION" in
        b)
            branch="$OPTARG"
            dirty=false
            ;;
        h)
            echo "Usage: $(basename $0) [-d] [-b BRANCH]"
            exit 0
            ;;
        ?)
            echo "Usage: $(basename $0) [-d] [-b BRANCH]"
            exit 1
    esac
done

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
version="$(rpmspec -P ${gittop}/${name}.spec | grep ^Version  | tr -s ' ' | cut -d' ' -f 2)"
prefix="${name}-${version}"
tarball="${gittop}/${name}-${version}.tar.gz"

set -ex
rm -fv ${tarball}
if $dirty; then
    cd $gittop && \
    tar \
        --transform="s,^,${prefix}/," \
        -cvzf $tarball \
        *
else
    git archive \
        --format=tgz \
        --prefix=${prefix}/ ${branch} \
        > ${tarball}
fi
