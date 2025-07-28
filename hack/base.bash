#!/usr/bin/env bash

# Common library functions for Red Hat CI Ansible OpenShift Collection
#
# Provides logging, OS detection, version comparison and other utilities
# for Ansible collection maintenance and testing.

function util.validate_bash() {
  _validate_bash_basic
  return $?
}

function _validate_bash_basic() {
  local \
    os \
    arch \
    path_line
  os="$(uname -s || true)"
  arch="$(uname -m || true)"
  # Test nameref support - this test is bash 3.2 compatible
  # shellcheck disable=SC2034
  if ! (declare -n test_ref 2>/dev/null); then
    {
      echo "ERROR: This library requires Bash 4.3+ for nameref support."
      echo "Current Bash version: ${BASH_VERSION}"
      echo ""
    } >&2
    if [[ "${os}" == "Linux" ]]; then
      {
        echo "Please update to a system with higher version of Bash, or"
        echo "make sure a compatible version of bash is on PATH"
      } >&2
      exit 1
    fi
    if [[ "${os}" == "Darwin" ]]; then
      # intel silicon
      if [[ "${arch}" == "arm64" ]]; then
        # apple silicon
        path_line="export PATH=\"/opt/homebrew/bin:\${PATH}\" # Apple Silicon"
      else
        # intel silicon
        path_line="export PATH=\"/usr/local/bin:\${PATH}\" # Intel Silicon"
      fi
      {
        echo "macOS fix:"
        echo "  brew install bash"
        echo "  ${path_line}"
        echo ""
        echo "Add PATH export to ~/.zshrc and restart terminal."
      } >&2
      exit 1
    fi
  fi
  return 0
}

_validate_bash_basic # fail early if bash is too old

SCRIPT_DEBUG="${SCRIPT_DEBUG:-"0"}"
FIND="${FIND:-"find"}"
GREP="${GREP:-"grep"}"
SED="${SED:-"sed"}"
OS="${OS:-"$(uname -s || true)"}"
DO_NOT_EXIT="${DO_NOT_EXIT:-"0"}"
LOG_LEVEL="${LOG_LEVEL:-""}"

# Initialize LEVELS_MAP if it's not already defined
if declare -p LEVELS_MAP 2>/dev/null && [[ "$(declare -p LEVELS_MAP)" =~ "declare -A" ]]; then
  : # already defined, do nothing
else
  declare -A LEVELS_MAP
  LEVELS_MAP["TRACE"]=0
  LEVELS_MAP["DEBUG"]=10
  LEVELS_MAP["INFO"]=20
  LEVELS_MAP["WARNING"]=30
  LEVELS_MAP["ERROR"]=40
  LEVELS_MAP["FATAL"]=50
  readonly LEVELS_MAP
fi

# shell-safe joiner that treats the delimiter as plain text
function txt.join_by() {
  local delimiter result elem
  delimiter="${1?cannot continue without delimiter}"
  shift 1
  result=""
  for elem in "${@}"; do
    result+="${elem}${delimiter}"
  done
  printf '%s' "${result%"${delimiter}"}"
  return 0
}

function txt.contains_element() {
  local seeking="${1?cannot continue without seeking}"
  shift 1
  local -a arr=("${@}")
  for element in "${arr[@]}"; do
    test "${element}" = "${seeking}" && return 0
  done
  return 1
}

function log.init() {
  local level="${1:-""}"
  level="${level^^}"
  if [[ -z "${level}" ]]; then
    case "${SCRIPT_DEBUG}" in
      0) LOG_LEVEL="INFO" ;;
      1) LOG_LEVEL="DEBUG" ;;
      2) LOG_LEVEL="TRACE" ;;
      *) LOG_LEVEL="INFO" ;;
    esac
    return 0
  fi
  txt.contains_element "${level}" "${!LEVELS_MAP[@]}" && LOG_LEVEL="${level}" && return 0
  # Set a valid LOG_LEVEL before logging the error to avoid infinite recursion
  LOG_LEVEL="FATAL"
  log.fatal "LOG_LEVEL='${level}' is invalid. Valid values are: $(txt.join_by ", " "${!LEVELS_MAP[@]}" || true)" >&2
  test "${DO_NOT_EXIT}" -eq 0 && exit 1
  return 1
}

function log.set_level() {
  local level="${1?cannot continue without level}"
  level="${level^^}"
  txt.contains_element "${level}" "${!LEVELS_MAP[@]}" && LOG_LEVEL="${level}" && return 0
  log.die 1 "Invalid log level: '${level}'. Valid levels are: $(txt.join_by ", " "${!LEVELS_MAP[@]}" || true)"
  return $?  # Propagate log.die's return code when DO_NOT_EXIT=1
}

function log.msg() {
  local level set_level_value current_level_value err_msg ts descriptor
  local -a msg
  level="${1?cannot continue without level}"
  level="${level^^}"
  shift 1
  msg=("${@}")
  ts="$(date -u || true)"
  test "${#msg[@]}" -eq 0 && return 0
  err_msg="is invalid. Valid values are: $(txt.join_by ", " "${!LEVELS_MAP[@]}" || true)"
  # test LOG_LEVEL was set to invalid value (LOG_LEVEL is not readonly)
  txt.contains_element "${LOG_LEVEL}" "${!LEVELS_MAP[@]}" || log.die 1 "LOG_LEVEL='${LOG_LEVEL}' ${err_msg}"
  # test ${level} is a valid log level (just in case - should never happen)
  txt.contains_element "${level}" "${!LEVELS_MAP[@]}" || log.die 1 "level='${level}' ${err_msg}"
  # Here ${level} is ALWAYS a valid log level
  set_level_value="${LEVELS_MAP[${level}]}"
  current_level_value="${LEVELS_MAP[${LOG_LEVEL}]}"
  test "${set_level_value}" -lt "${current_level_value}" && return 0
  descriptor=2
  if [[ "${level}" = "INFO" ]]; then descriptor=1; fi
  echo -e "${ts} - ${level} - ${msg[*]}" >&"${descriptor}"
  return 0
}

function log.trace() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.debug() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.info() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.warning() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.error() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.fatal() {
  local level="${FUNCNAME[0]}"; local -a msg=("${@}");log.msg "${level##*.}" "${msg[@]}"; return $?
}

function log.die() {
  local rc msg
  rc="${1?cannot continue without rc}"
  shift 1
  msg="${*}"
  log.fatal "${msg}"
  test "${DO_NOT_EXIT}" -gt 0 && return "${rc}"
  exit "${rc}"
}

function prolog() {
  local func_name="${FUNCNAME[1]}"
  log.trace "Inside ${func_name}()\nThe call (debug) was: '${FUNCNAME[1]} ${*}'\n"
  return 0
}

function epilog() {
  local name="${FUNCNAME[1]}";
  local rc="${1?cannot continue without rc}"
  shift 1
  local -a msg=("Function ${name}()")
  msg+=("${@}" "completed with rc=${rc}")
  log.trace "${msg[@]}"
}

function app.run() {
  local expected_rc="${1?cannot continue without expected_rc}"; shift 1
  local -a cmd=("${@}")
  local rc=1
  prolog "${expected_rc}" "${cmd[@]}"
  test "${#cmd[@]}" -eq 0 && log.die "${rc}" "The command '${cmd[*]}' cannot be empty"
  log.debug "About to run command: '${cmd[*]}'"
  "${cmd[@]}" && rc=$? || rc=$?
  test "${rc}" -eq "${expected_rc}" || log.die "${rc}" "The command '${cmd[*]}' returned unexpected rc=${rc}. [EXPECTED: ${expected_rc}]"
  epilog "${rc}"
  return "${rc}"
}

function app.validate() {
  local app rc
  app="${1?cannot continue without app}"
  if ! command -v "${app}" &>/dev/null; then
    log.fatal "${app} is not installed."
    return 1
  fi
  return 0
}

function utils.tools_setup() {
  local os="${1:-"${OS}"}"
  local rc=1
  prolog "${@}"
  log.debug "Running on ${os}"
  case "${os}" in
  Linux)
    app.validate grep || log.die "${rc}" "Install it with 'sudo [dnf|yum|apt] -y install grep'"
    GREP="grep"
    app.validate find || log.die "${rc}" "Install it with 'sudo [dnf|yum|apt] -y install findutils'"
    FIND="find"
    app.validate sed || log.die "${rc}" "Install it with 'sudo [dnf|yum|apt] -y install sed'"
    SED="sed"
    rc=0
    ;;
  Darwin)
    app.validate ggrep || log.die "${rc}" "Install it with 'brew install grep'"
    GREP="ggrep"
    app.validate gfind || log.die "${rc}" "Install it with 'brew install findutils'"
    FIND="gfind"
    app.validate gsed || log.die "${rc}" "Install it with 'brew install gnu-sed'"
    SED="gsed"
    rc=0
    ;;
  *)
    log.die "${rc}" "Unsupported OS: ${os}"
    ;;
  esac
  return "${rc}"
}

if [[ "${BASH_SOURCE[0]}" = "${0}" ]]; then
  log.fatal "This script is not meant to be run directly"
  log.fatal "Usage: source ${BASH_SOURCE[0]}"
  exit 1
fi
log.init "${LOG_LEVEL}" || return $?
utils.tools_setup "${OS}"
### END OF BASE.BASH ###
