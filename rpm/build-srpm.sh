#!/bin/bash

org=redhatci
repo=ocp
name="ansible-collection-${org}-${repo}"
gittop="$(git rev-parse --show-toplevel)"
sourcedir="$(rpm --eval "%{_sourcedir}")"
srpmdir="$(rpm --eval "%{_srcrpmdir}")"

set -ex
mv -fv ${gittop}/${name}-*.tar.gz ${sourcedir}/
cp -fv ${gittop}/build_ignore.patch ${sourcedir}/
rpmbuild -bs ${gittop}/${name}.spec
