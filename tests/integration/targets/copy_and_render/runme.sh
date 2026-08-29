#!/bin/bash

set -eu

dir=$(dirname "$0")

# Case 1: absolute source path
ansible-playbook -v -i "$dir/../../inventory" -e car_source_dir="$dir/files" "$dir/copy_and_render.yml"

# Case 2: source path using "~" notation (regression test).
# The find module expands "~" in its paths, so the role must expanduser
# car_source_dir too, otherwise the derived destination path is corrupted.
# The "~" is kept literal (quoted) so only the role expands it.
tilde_src="car_render_tilde_test_$$"
cleanup() {
    rm -rf "${HOME:?}/$tilde_src"
}
trap cleanup EXIT

mkdir -p "$HOME/$tilde_src"
cp -a "$dir/files/." "$HOME/$tilde_src/"

ansible-playbook -v -i "$dir/../../inventory" -e car_source_dir="~/$tilde_src" "$dir/copy_and_render.yml"

# Case 3: relative source path using "./" notation (regression test).
# The find module strips a leading "./" from the paths it returns, so the
# role must strip it from src_dir too. Run from the target dir so "./files"
# resolves for both the copy (playbook basedir) and find (process cwd) steps.
(cd "$dir" && ansible-playbook -v -i "../../inventory" -e car_source_dir="./files" copy_and_render.yml)

# runme.sh ends here
