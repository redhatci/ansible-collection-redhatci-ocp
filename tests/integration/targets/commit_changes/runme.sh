#!/bin/bash

dir=$(dirname "$0")

exec ansible-playbook -v -i $dir/../../inventory commit_changes.yml

# runme.sh ends here
