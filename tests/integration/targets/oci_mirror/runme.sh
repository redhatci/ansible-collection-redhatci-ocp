#!/bin/bash

set -euo pipefail

dir=$(dirname "$0")

exec ansible-playbook -v -i "$dir/../../inventory" "$dir/oci_mirror.yml"

# runme.sh ends here
