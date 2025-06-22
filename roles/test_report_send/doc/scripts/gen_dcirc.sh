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

# die prints the given message and exits the script with the specified return code.
function die() { rc="${1?no rc passed}"; shift 1; echo "${*}"; exit "${rc}"; }

# ensure_apps checks that each specified command is available in the system PATH, exiting with an error if any are missing.
function ensure_apps() {
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
# print_file displays the contents of the specified file, surrounded by delimiter lines, with a header indicating the file name.
function print_file() {
  local out
  out="${1:-"dcirc.sh"}"
  echo "file ${out} generated with the following contents:"
  echo "----8<--------8<--------8<--------8<--------8<--------8<--------8<--------8<----"
  cat "${out}"
  echo "---->8-------->8-------->8-------->8-------->8-------->8-------->8-------->8----"
}

# gen_dcirc_sh generates a shell script file that sets and exports specified environment variables, preventing overwriting if the file already exists.
function gen_dcirc_sh() {
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

# main generates a dcirc.sh file with required environment variables for dcictl, creating random values if not already set, and prints the file contents.
function main() {
  local \
    out
  local -a \
    vars
  out="dcirc.sh"
  ensure_apps uuidgen

  # Generate the random string in the right format:
  test -n "${DCI_API_SECRET}" || DCI_API_SECRET="$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c "${LEN}" || true)"
  vars+=(DCI_API_SECRET)

  # Generate UUID
  test -n "${DCI_CLIENT_ID}" || DCI_CLIENT_ID="${PREFIX}/$(uuidgen | tr '[:upper:]' '[:lower:]' || true)"
  vars+=(DCI_CLIENT_ID)

  test -n "${DCI_CS_URL}" || DCI_CS_URL="https://api.distributed-ci.io/"
  vars+=(DCI_CS_URL)

  gen_dcirc_sh "${out}" "${vars[@]}"
  print_file "${out}"
  return $?
}

main "${@}"
exit $?
