#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

function gen_node_labels() {
  # gen_node_labels()
  #  - outputs node labels describing the host's operating system, CPU architecture,
  #    and available container engines as a space-separated string.
  local \
    os \
    arch \
    item
  local -a \
    results \
    archs \
    container_engines
  os="$(uname -s | tr '[:upper:]' '[:lower:]' || true)"
  results+=("os:${os}")
  arch="$(uname -m | tr '[:upper:]' '[:lower:]' || true)"
  archs+=("${arch}")
  if [[ "${arch}" = "x86_64" ]]; then
    archs+=("amd64")
  fi
  for arch in "${archs[@]}"; do
    results+=("arch:${arch}")
  done
  if command -v docker > /dev/null; then
    container_engines+=("docker")
  fi
  if command -v podman > /dev/null; then
    container_engines+=("podman")
  fi
  for item in "${container_engines[@]}"; do
    results+=("containers:${item}")
  done
  echo "${results[*]}"
  return 0
}

gen_node_labels
exit $?