#!/usr/bin/env bash
########################################################################################################################
# This script generates properly formatted sample dcirc.sh file used by dcictl
########################################################################################################################
set -o pipefail
set -o errexit
PREFIX="${PREFIX:-"remoteci"}"
LEN="${LEN:-"64"}"
DCI_API_SECRET="${DCI_API_SECRET:-""}"
DCI_CLIENT_ID="${DCI_CLIENT_ID:-""}"
DCI_CS_URL="${DCI_CS_URL:-""}"

function die() {
  # die() prints the given message and exits the script with the specified return code.
  local \
    rc
  rc="${1?no rc passed}";
  shift 1;
  echo "${*}";
  exit "${rc}";
}

function ensure_apps() {
  # ensure_apps() checks if the given apps are on the PATH and exits the script with an error if not.
  local -a \
    apps
  local \
    app \
    rc
  apps=("${@}")
  for app in "${apps[@]}"; do
    if ! command -v "${app}" >/dev/null 2>/dev/null; then
      rc=$?
      die "${rc}" "FATAL: command ${app} not on PATH, install it"
    fi
  done
  return 0
}

function print_file() {
  # print_file() prints the contents of the given file.
  local out
  out="${1:-"dcirc.sh"}"
  echo "file ${out} generated with the following contents:"
  echo "----8<--------8<--------8<--------8<--------8<--------8<--------8<--------8<----"
  cat "${out}"
  echo "---->8-------->8-------->8-------->8-------->8-------->8-------->8-------->8----"
}

function gen_dcirc_sh() {
  # gen_dcirc_sh()
  #  - safely generates a shell script file that sets and exports specified environment variables
  local \
    out \
    rc \
    var_name \
    var_value
  local -a \
    vars
  out="${1:-"dcirc.sh"}"
  shift 1
  vars=("${@}")
  if [[ "${#vars[@]}" -eq 0 ]]; then
    vars+=(
      DCI_CLIENT_ID
      DCI_API_SECRET
      DCI_CS_URL
    )
  fi
  if [[ -r "${out}" ]]; then
    rc=1
    die "${rc}" "FATAL: cannot continue. [REASON: '${out}' already exists. Back it up and rename first.]"
  fi
  if ! touch "${out}"; then
    rc=$?
    die "${rc}" "failed to create ${out}"
  fi
  {
    for var_name in "${vars[@]}"; do
      var_value="$(eval "echo \"\${${var_name}}\"")"
      echo "${var_name}='${var_value}'"
    done
    echo "export ${vars[*]}"
  } >"${out}"
  return 0  
}

function main() {
  # main generates a dcirc.sh file with required environment variables for dcictl
  # it creates random values if corresponding variables are not set already
  # and prints the file contents
  # beware: the console output can be seen by anybody
  local \
    out
  local -a \
    vars
  out="dcirc.sh"
  ensure_apps uuidgen

  # Generate the random string in the right format if DCI_API_SECRET is not set
  test -n "${DCI_API_SECRET}" || DCI_API_SECRET="$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c "${LEN}" || true)"
  vars+=(DCI_API_SECRET)

  # Generate UUID if DCI_CLIENT_ID is not set
  test -n "${DCI_CLIENT_ID}" || DCI_CLIENT_ID="${PREFIX}/$(uuidgen | tr '[:upper:]' '[:lower:]' || true)"
  vars+=(DCI_CLIENT_ID)

  # Use default DCI_CS_URL if it is not set
  test -n "${DCI_CS_URL}" || DCI_CS_URL="https://api.distributed-ci.io/"
  vars+=(DCI_CS_URL)

  gen_dcirc_sh "${out}" "${vars[@]}"
  print_file "${out}"
  return $?
}

main "${@}"
exit $?
