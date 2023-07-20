#!/bin/bash -x

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
sourcedir="$(rpm --eval "%{_sourcedir}")"

cp -fv ${gittop}/${name}-*.tar.gz ${sourcedir}/
cp -fv ${gittop}/rpm/build_ignore.patch ${sourcedir}/
rpmbuild -bs ${gittop}/ansible-collection-redhat-ocp.spec
