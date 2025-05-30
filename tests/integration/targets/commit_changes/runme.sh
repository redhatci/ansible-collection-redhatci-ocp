#!/bin/bash

dir=$(dirname "$0")

if [ -r $dir/../../inventory ]; then
    INV="-i $dir/../../inventory"
else
    INV=
fi

exec ansible-playbook -v $INV commit_changes.yml

# runme.sh ends here
