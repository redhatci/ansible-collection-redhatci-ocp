#!/bin/bash

dir=$(dirname "$0")

exec ansible-playbook -v -i $dir/../../inventory $dir/oci_mirror_manifests.yml

# runme.sh ends here
