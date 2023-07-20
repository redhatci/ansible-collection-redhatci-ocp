#!/bin/bash -x

dirty=false
branch="main"
while getopts ':db:' OPTION; do
    case "$OPTION" in
        d)
            dirty=true
            ;;
        b)
            branch="$OPTARG"
            ;;
        ?)
            echo "Usage: $(basename $0) [-d] [-b BRANCH]"
    esac
done

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
version="$(grep ^Version ${gittop}/${name}.spec | tr -s ' ' | cut -d' ' -f 2)"
prefix="${name}-${version}"
tarball="${gittop}/${name}-${version}.tar.gz"

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
