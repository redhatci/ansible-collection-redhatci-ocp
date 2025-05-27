#!/bin/bash

dir=$(dirname "$0")

exec ansible-playbook -v -i $dir/../../inventory -e car_source_dir=$dir/files $dir/copy_and_render.yml

# runme.sh ends here
