#!/usr/bin/env bash

# Common library functions for Red Hat CI Ansible OpenShift Collection
#
# Provides logging, OS detection, version comparison and other utilities
# for Ansible collection maintenance and testing.

SCRIPT_DEBUG="${SCRIPT_DEBUG:-"0"}"
GREP="${GREP:-"grep"}"
SED="${SED:-"sed"}"
LIVE_FOREVER="${LIVE_FOREVER:-"0"}"
OS="$(uname -s || true)"

declare -A LEVELS_MAP
LEVELS_MAP["TRACE"]=0
LEVELS_MAP["DEBUG"]=10
LEVELS_MAP["INFO"]=20
LEVELS_MAP["WARNING"]=30
LEVELS_MAP["ERROR"]=40
LEVELS_MAP["FATAL"]=50

LOG_LEVEL="${LOG_LEVEL:-""}"

if [[ -z "${LOG_LEVEL}" ]]; then
  case "${SCRIPT_DEBUG}" in
    0) LOG_LEVEL="INFO" ;;
    1) LOG_LEVEL="DEBUG" ;;
    2) LOG_LEVEL="TRACE" ;;
    *) LOG_LEVEL="INFO" ;;
  esac
else
  LOG_LEVEL="${LOG_LEVEL^^}"
fi

#######################################
# Join array elements with delimiter
# Arguments:
#   $1 - Delimiter to use between elements
#   $2+ - Array elements to join
# Outputs:
#   Writes joined string with delimiter between elements to stdout
#######################################
function join_by() {
  local \
    delimiter \
    result
  delimiter="${1?cannot continue without delimiter}"
  shift 1
  printf -v result "%s${delimiter}" "${@}"
  echo "${result%"${delimiter}"}"
  return 0
}

#######################################
# Check if array contains specific element
# Arguments:
#   $1 - Element to search for
#   $2+ - Array elements to search in
# Returns:
#   0 if element found in array, 1 if not found
#######################################
function contains_element() {
  local seeking="${1?cannot continue without seeking}"
  shift 1
  local -a arr=("${@}")
  for element in "${arr[@]}"; do
    if [[ "${element}" = "${seeking}" ]]; then
      return 0
    fi
  done
  return 1
}

#######################################
# Set the global log level for message filtering
# Globals:
#   LOG_LEVEL - Set to the provided log level
# Arguments:
#   $1 - Log level (TRACE, DEBUG, INFO, WARNING, ERROR, FATAL)
# Returns:
#   0 on success, calls die() on invalid level
#######################################
function log.set_level() {
  local level
  level="${1?cannot continue without level}"
  level="${level^^}"
  if ! contains_element "${level}" "${!LEVELS_MAP[@]}"; then
    die 1 "Invalid log level: ${level}"
  fi
  LOG_LEVEL="${level}"
  return 0
}

#######################################
# Log a message at the specified level with timestamp
# Arguments:
#   $1 - Log level (TRACE, DEBUG, INFO, WARNING, ERROR, FATAL)
#   $2+ - Message components to log
# Outputs:
#   INFO messages to stdout, all others to stderr (with timestamp)
#######################################
function log.msg() {
  local \
    level \
    set_level_value \
    current_level_value \
    ts
  local -a msg
  level="${1?cannot continue without level}"
  level="${level^^}"
  shift 1
  msg=("${@}")
  set_level_value="${LEVELS_MAP[${level}]}"
  current_level_value="${LEVELS_MAP[${LOG_LEVEL}]}"
  if [[ "${set_level_value}" -lt "${current_level_value}" ]]; then
    return 0
  fi
  if [[ "${#msg[@]}" -eq 0 ]]; then
    return 0
  fi
  ts="$(date -u || true)"
  if [[ "${level}" != "INFO" ]]; then
    echo -e "${ts} - ${level} - ${msg[*]}" >&2
  else
    echo -e "${ts} - ${level} - ${msg[*]}"
  fi
  return 0
}

#######################################
# Log a trace message (lowest priority)
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Trace message with timestamp to stderr (if LOG_LEVEL=TRACE)
#######################################
function log.trace() {
  local level="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${level##*.}" "${msg[@]}"
  return $?
}

#######################################
# Log a debug message
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Debug message with timestamp to stderr (if LOG_LEVEL=DEBUG or lower)
#######################################
function log.debug() {
  local level="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${level##*.}" "${msg[@]}"
  return $?
}

#######################################
# Log an info message
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Info message with timestamp to stdout (if LOG_LEVEL=INFO or lower)
#######################################
function log.info() {
  local level="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${level##*.}" "${msg[@]}"
  return $?
}

#######################################
# Log a warning message
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Warning message with timestamp to stderr
#######################################
function log.warning() {
  local op="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${op##*.}" "${msg[@]}"
  return $?
}

#######################################
# Log an error message
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Error message with timestamp to stderr
#######################################
function log.error() {
  local level="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${level##*.}" "${msg[@]}"
  return $?
}

#######################################
# Log a fatal message
# Arguments:
#   $1+ - Message components to log
# Outputs:
#   Fatal message with timestamp to stderr
#######################################
function log.fatal() {
  local level="${FUNCNAME[0]}"
  local -a msg=("${@}")
  log.msg "${level##*.}" "${msg[@]}"
  return $?
}

#######################################
# Print message and exit with return code (or return if LIVE_FOREVER=1)
# Globals:
#   LIVE_FOREVER - If non-zero, returns instead of exiting
# Arguments:
#   $1 - Exit code to use
#   $2+ - Message to log as fatal before exiting
# Outputs:
#   Fatal message with timestamp to stderr
# Returns:
#   Exits with provided code (if LIVE_FOREVER=0) or returns code
#######################################
function die() {
  local rc msg
  rc="${1?cannot without rc}"
  shift 1
  msg="${*}"
  log.fatal "${msg}"
  if [[ "${LIVE_FOREVER}" -ne 0 ]]; then
    return "${rc}"
  fi
  exit "${rc}"
}

#######################################
# Print function entry debug info
# Arguments:
#   $1+ - Function arguments to log
# Outputs:
#   Debug trace of function entry to stderr (if LOG_LEVEL=TRACE)
#######################################
function prolog() {
  local \
    func_name \
    msg
  func_name="${FUNCNAME[1]}"
  log.trace "Inside ${func_name}()\nThe call (debug) was: '${FUNCNAME[1]} ${*}'\n"
  return 0
}

#######################################
# Print function exit debug info
# Arguments:
#   $1 - Return code of function
#   $2+ - Additional completion message
# Outputs:
#   Debug trace of function exit to stderr (if LOG_LEVEL=TRACE)
#######################################
function epilog() {
  local \
    name \
    rc
  local -a msg
  name="${FUNCNAME[1]}"
  rc="${1?cannot continue without rc}"
  shift 1
  msg=("Function ${name}()")
  msg+=("${@}")
  msg+=("completed with rc=${rc}")
  log.trace "${msg[@]}"
}

#######################################
# Run command and verify expected return code
# Arguments:
#   $1 - Expected return code
#   $2+ - Command and arguments to execute
# Outputs:
#   Debug and error messages to stderr
# Returns:
#   Expected return code on success, calls die() on failure
#######################################
function run_cmd() {
  local -a \
    cmd
  local \
    expected_rc \
    rc
  prolog "${@}"
  expected_rc="${1?cannot continue without expected_rc}"
  shift 1
  cmd=("${@}")
  test "${#cmd[@]}" -ne 0 || die 1 "The command '${cmd[*]}' cannot be empty"
  log.debug "About to run command: '${cmd[*]}'"
  "${cmd[@]}"
  rc=$?
  test "${rc}" -eq "${expected_rc}" || die "${rc}" "The command '${cmd[*]}' returned unexpected rc=${rc}. [EXPECTED: ${expected_rc}]"
  epilog "${rc}"
  return "${rc}"
}

#######################################
# Setup OS-specific tool variables (SED, GREP)
# Globals:
#   SED - Set to 'sed' (Linux) or 'gsed' (Darwin)
#   GREP - Set to 'grep' (Linux) or 'ggrep' (Darwin)
# Arguments:
#   $1 - OS name (optional, defaults to detected OS)
# Outputs:
#   Debug and error messages to stderr
# Returns:
#   0 on success, calls die() on unsupported OS
#######################################
function tools_setup() {
  local os rc
  prolog "${@}"
  os="${1:-"${OS}"}"
  rc=1
  log.debug "Running on ${os}"
  case "${os}" in
    Linux) SED="sed"; GREP="grep" ;;
    Darwin) SED="gsed"; GREP="ggrep" ;;
    *) die "${rc}" "Unsupported OS: ${os}" ;;
  esac
  rc=0
  epilog "${rc}" "Running on ${os}. Selected: SED=${SED}, GREP=${GREP}"
  return 0
}

#######################################
# Compare two semantic version strings (supports pre-release and build metadata)
# Arguments:
#   $1 - Left version (e.g., "1.2.3", "2.0.0-alpha", "1.0.0+build")
#   $2 - Right version (e.g., "1.2.4", "2.0.0-beta", "1.0.0")
# Outputs:
#   Writes -1 if left < right, 0 if equal, 1 if left > right to stdout
# Note:
#   Follows semantic versioning rules where pre-release versions are < release versions
#   and pre-release precedence: alpha < beta < rc < (release)
#######################################
function compare_versions() {
  local \
    left \
    right \
    left_major \
    left_minor \
    left_patch_full \
    right_major \
    right_minor \
    right_patch_full \
    left_patch_num \
    left_prerelease \
    right_patch_num \
    right_prerelease

  left="${1?cannot continue without left}"
  right="${2?cannot continue without right}"

  # Remove build metadata (everything after +) for comparison
  left="${left%%+*}"
  right="${right%%+*}"

  # Split into major.minor.patch parts
  IFS='.' read -r left_major left_minor left_patch_full <<<"${left}"
  IFS='.' read -r right_major right_minor right_patch_full <<<"${right}"

  # Split patch into numeric part and pre-release part
  if [[ "${left_patch_full}" =~ ^([0-9]+)(-.*)?$ ]]; then
    left_patch_num="${BASH_REMATCH[1]}"
    left_prerelease="${BASH_REMATCH[2]#-}"  # Remove leading dash
  else
    left_patch_num="${left_patch_full}"
    left_prerelease=""
  fi

  if [[ "${right_patch_full}" =~ ^([0-9]+)(-.*)?$ ]]; then
    right_patch_num="${BASH_REMATCH[1]}"
    right_prerelease="${BASH_REMATCH[2]#-}"  # Remove leading dash
  else
    right_patch_num="${right_patch_full}"
    right_prerelease=""
  fi

  # Compare major versions
  if ((left_major > right_major)); then
    echo 1
    return 0
  elif ((left_major < right_major)); then
    echo -1
    return 0
  fi

  # Compare minor versions
  if ((left_minor > right_minor)); then
    echo 1
    return 0
  elif ((left_minor < right_minor)); then
    echo -1
    return 0
  fi

  # Compare patch versions (numeric part)
  if ((left_patch_num > right_patch_num)); then
    echo 1
    return 0
  elif ((left_patch_num < right_patch_num)); then
    echo -1
    return 0
  fi

  # Patch numbers are equal, now compare pre-release versions
  # Per SemVer: pre-release version has lower precedence than normal version
  if [[ -z "${left_prerelease}" && -n "${right_prerelease}" ]]; then
    echo 1  # left (release) > right (pre-release)
    return 0
  elif [[ -n "${left_prerelease}" && -z "${right_prerelease}" ]]; then
    echo -1  # left (pre-release) < right (release)
    return 0
  elif [[ -z "${left_prerelease}" && -z "${right_prerelease}" ]]; then
    echo 0  # Both are releases and equal
    return 0
  fi

  # Both have pre-release versions, compare them
  # Define precedence: alpha < beta < rc
  declare -A prerelease_order=(
    ["alpha"]=1
    ["beta"]=2
    ["rc"]=3
  )

  local left_order right_order
  left_order="${prerelease_order[${left_prerelease}]:-999}"
  right_order="${prerelease_order[${right_prerelease}]:-999}"

  if ((left_order < right_order)); then
    echo -1
  elif ((left_order > right_order)); then
    echo 1
  else
    # Same precedence or both unknown, compare lexically
    if [[ "${left_prerelease}" < "${right_prerelease}" ]]; then
      echo -1
    elif [[ "${left_prerelease}" > "${right_prerelease}" ]]; then
      echo 1
    else
      echo 0
    fi
  fi
}

if [[ "${BASH_SOURCE[0]}" = "${0}" ]]; then
  die 1 "This script is not meant to be run directly"
fi
