#!/usr/bin/env bats

bats_require_minimum_version 1.5.0

load ../common_lib.bash

# --- Unit Tests for compare_versions ---

@test "compare_versions returns 0 for identical versions (1.0 vs 1.0)" {
  # 'run' executes the command and captures its stdout, stderr, and exit status.
  # The output is stored in the '$output' variable.
  # The exit status is stored in the '$status' variable.
  run compare_versions "1.0" "1.0"
  expected="0"
  # Assert that the command exited successfully (status 0).
  [[ "${status}" -eq 0 ]]
  # Assert that the standard output matches the expected value.
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions returns 1 when first version is greater (1.1 vs 1.0)" {
  run compare_versions "1.1" "1.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions returns -1 when second version is greater (1.0 vs 1.1)" {
  run compare_versions "1.0" "1.1"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions returns 1 for major version difference (2.0 vs 1.9)" {
  run compare_versions "2.0" "1.9"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions returns 0 for identical patch versions (1.5 vs 1.5)" {
  run compare_versions "1.5" "1.5"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions handles empty strings as 0" {
  run compare_versions "" ""
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions empty string vs version" {
  run compare_versions "" "1.0"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions version vs empty string" {
  run compare_versions "1.0" ""
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions with leading zeros (01.02 vs 1.2)" {
  run compare_versions "01.02" "1.2"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions with differing segment lengths and zeros" {
  run compare_versions "1.0" "1"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions with different major versions" {
  run compare_versions "3.0" "2.99"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

# --- Semantic Versioning Tests (Pre-release and Build Metadata) ---

@test "compare_versions: pre-release should be less than release (2.0.0-alpha vs 2.0.0)" {
  run compare_versions "2.0.0-alpha" "2.0.0"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: alpha should be less than beta (2.0.0-alpha vs 2.0.0-beta)" {
  run compare_versions "2.0.0-alpha" "2.0.0-beta"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: RC should be less than release (2.0.0-rc vs 2.0.0)" {
  run compare_versions "2.0.0-rc" "2.0.0"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: build metadata should be ignored (2.0.0 vs 2.0.0+build)" {
  run compare_versions "2.0.0" "2.0.0+build"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: beta should be less than RC (2.0.0-beta vs 2.0.0-rc)" {
  run compare_versions "2.0.0-beta" "2.0.0-rc"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: alpha should be less than RC (2.0.0-alpha vs 2.0.0-rc)" {
  run compare_versions "2.0.0-alpha" "2.0.0-rc"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: beta should be greater than alpha (2.0.0-beta vs 2.0.0-alpha)" {
  run compare_versions "2.0.0-beta" "2.0.0-alpha"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: RC should be greater than beta (2.0.0-rc vs 2.0.0-beta)" {
  run compare_versions "2.0.0-rc" "2.0.0-beta"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: RC should be greater than alpha (2.0.0-rc vs 2.0.0-alpha)" {
  run compare_versions "2.0.0-rc" "2.0.0-alpha"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: release should be greater than pre-release (2.0.0 vs 2.0.0-alpha)" {
  run compare_versions "2.0.0" "2.0.0-alpha"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: release should be greater than pre-release beta (2.0.0 vs 2.0.0-beta)" {
  run compare_versions "2.0.0" "2.0.0-beta"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: release should be greater than pre-release RC (2.0.0 vs 2.0.0-rc)" {
  run compare_versions "2.0.0" "2.0.0-rc"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: equal pre-releases alpha (2.0.0-alpha vs 2.0.0-alpha)" {
  run compare_versions "2.0.0-alpha" "2.0.0-alpha"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: equal pre-releases beta (2.0.0-beta vs 2.0.0-beta)" {
  run compare_versions "2.0.0-beta" "2.0.0-beta"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: equal pre-releases RC (2.0.0-rc vs 2.0.0-rc)" {
  run compare_versions "2.0.0-rc" "2.0.0-rc"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: different build metadata should be ignored (1.0.0+build1 vs 1.0.0+build2)" {
  run compare_versions "1.0.0+build1" "1.0.0+build2"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: build metadata vs no metadata (1.0.0+build vs 1.0.0)" {
  run compare_versions "1.0.0+build" "1.0.0"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: pre-release with build metadata (2.0.0-alpha+build vs 2.0.0-alpha)" {
  run compare_versions "2.0.0-alpha+build" "2.0.0-alpha"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: pre-release with different build metadata (2.0.0-alpha+build1 vs 2.0.0-alpha+build2)" {
  run compare_versions "2.0.0-alpha+build1" "2.0.0-alpha+build2"
  expected="0"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: unknown pre-release labels lexical comparison (2.0.0-gamma vs 2.0.0-delta)" {
  run compare_versions "2.0.0-gamma" "2.0.0-delta"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: unknown pre-release labels lexical comparison 2 (2.0.0-custom1 vs 2.0.0-custom2)" {
  run compare_versions "2.0.0-custom1" "2.0.0-custom2"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: known vs unknown pre-release precedence (2.0.0-alpha vs 2.0.0-gamma)" {
  run compare_versions "2.0.0-alpha" "2.0.0-gamma"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: unknown vs known pre-release lexical vs precedence (2.0.0-zeta vs 2.0.0-beta)" {
  run compare_versions "2.0.0-zeta" "2.0.0-beta"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: multi-digit major version (10.0.0 vs 2.0.0)" {
  run compare_versions "10.0.0" "2.0.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: multi-digit minor version (1.10.0 vs 1.2.0)" {
  run compare_versions "1.10.0" "1.2.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: multi-digit patch version (1.0.10 vs 1.0.2)" {
  run compare_versions "1.0.10" "1.0.2"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: pre-release with dot notation lexical (2.0.0-alpha.1 vs 2.0.0-alpha.2)" {
  run compare_versions "2.0.0-alpha.1" "2.0.0-alpha.2"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: different pre-release types with dot notation (2.0.0-beta.1 vs 2.0.0-alpha.2)" {
  run compare_versions "2.0.0-beta.1" "2.0.0-alpha.2"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: very small versions (0.0.1 vs 0.0.2)" {
  run compare_versions "0.0.1" "0.0.2"
  expected="-1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: major version takes precedence over pre-release (3.0.0-alpha vs 2.0.0)" {
  run compare_versions "3.0.0-alpha" "2.0.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: minor version takes precedence over pre-release (2.1.0-alpha vs 2.0.0)" {
  run compare_versions "2.1.0-alpha" "2.0.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "compare_versions: patch version takes precedence over pre-release (2.0.1-alpha vs 2.0.0)" {
  run compare_versions "2.0.1-alpha" "2.0.0"
  expected="1"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

tools_setup_and_print_vars() {
  local rc os
  local -a \
    items
  os="${1}"
  shift 1
  items=("${@}")

  # Redirect log output to avoid interfering with variable output
  tools_setup "${os}" 2>/dev/null
  rc=$?
  for item in "${items[@]}"; do
    echo "${item}='$(eval echo "\${${item}}" || true)'"
  done
  return "${rc}"
}

@test "test os_setup('Linux') assigning SED=sed and GREP=grep" {
  OS="Linux"
  SED="sed"
  GREP="grep"
  declare -A expected
  expected[SED]="sed"
  expected[GREP]="grep"
  run tools_setup_and_print_vars "${OS}" "SED" "GREP"
  [[ "${status}" -eq 0 ]]
  eval "${output}"
  [[ "${SED}" = "${expected[SED]}" ]]
  [[ "${GREP}" = "${expected[GREP]}" ]]
}

@test "test os_setup('Darwin') assigning SED=gsed and GREP=ggrep" {
  OS="Darwin"
  SED="sed"
  GREP="grep"
  declare -A expected
  expected[SED]="gsed"
  expected[GREP]="ggrep"
  run tools_setup_and_print_vars "${OS}" "SED" "GREP"
  [[ "${status}" -eq 0 ]]
  eval "${output}"
  [[ "${SED}" = "${expected[SED]}" ]]
  [[ "${GREP}" = "${expected[GREP]}" ]]
}

@test "test os_setup on Unsupported OS to fail" {
  # Test tools_setup directly since we expect it to fail and need the stderr
  run --separate-stderr tools_setup "OpenBSD"
  [[ "${status}" -eq 1 ]]
  # shellcheck disable=SC2154
  [[ "${stderr}" =~ .*Unsupported\ OS:\ OpenBSD ]]
}

# --- Unit Tests for log.msg basic functionality ---

@test "log.msg INFO prints to stdout" {
  run log.msg "info" "This is an info message"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*This\ is\ an\ info\ message ]]
}

@test "log.msg ERROR prints to stderr" {
  run --separate-stderr log.msg "error" "This is an error message"
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*This\ is\ an\ error\ message ]]
  [[ "${output}" == "" ]]
}

@test "log.msg WARNING prints to stderr" {
  run --separate-stderr log.msg "warning" "This is a warning message"
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*This\ is\ a\ warning\ message ]]
  [[ "${output}" == "" ]]
}

@test "log.msg FATAL prints to stderr" {
  run --separate-stderr log.msg "fatal" "This is a fatal message"
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*FATAL.*This\ is\ a\ fatal\ message ]]
  [[ "${output}" == "" ]]
}

# --- Tests for SCRIPT_DEBUG behavior (when LOG_LEVEL is not manually overridden) ---

@test "SCRIPT_DEBUG=0 sets LOG_LEVEL=INFO" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=0 source ./common_lib.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=INFO ]]
}

@test "SCRIPT_DEBUG=1 sets LOG_LEVEL=DEBUG" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=1 source ./common_lib.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

@test "SCRIPT_DEBUG=2 sets LOG_LEVEL=TRACE" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=2 source ./common_lib.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=TRACE ]]
}

@test "SCRIPT_DEBUG=invalid sets LOG_LEVEL=INFO (default)" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=99 source ./common_lib.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=INFO ]]
}

# --- Tests for level filtering (message level vs LOG_LEVEL comparisons) ---

@test "TRACE message prints when LOG_LEVEL=TRACE" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level TRACE && log.msg trace "Trace message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*TRACE.*Trace\ message ]]
}

@test "TRACE message filtered when LOG_LEVEL=DEBUG" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level DEBUG && log.msg trace "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "DEBUG message prints when LOG_LEVEL=DEBUG" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level DEBUG && log.msg debug "Debug message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*DEBUG.*Debug\ message ]]
}

@test "DEBUG message filtered when LOG_LEVEL=INFO" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level INFO && log.msg debug "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "INFO message prints when LOG_LEVEL=INFO" {
  run bash -c 'source ./common_lib.bash && log.set_level INFO && log.msg info "Info message"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*Info\ message ]]
}

@test "INFO message filtered when LOG_LEVEL=WARNING" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level WARNING && log.msg info "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "WARNING message prints when LOG_LEVEL=WARNING" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level WARNING && log.msg warning "Warning message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*Warning\ message ]]
}

@test "WARNING message prints when LOG_LEVEL=INFO (higher level always prints)" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level INFO && log.msg warning "Warning message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*Warning\ message ]]
}

@test "ERROR message prints when LOG_LEVEL=ERROR" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level ERROR && log.msg error "Error message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Error\ message ]]
}

@test "ERROR message prints when LOG_LEVEL=INFO (higher level always prints)" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level INFO && log.msg error "Error message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Error\ message ]]
}

@test "FATAL message always prints regardless of LOG_LEVEL" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level FATAL && log.msg fatal "Fatal message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*FATAL.*Fatal\ message ]]
}

@test "log.msg handles multiple message arguments" {
  run --separate-stderr log.msg "error" "Multiple" "message" "arguments"
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Multiple\ message\ arguments ]]
}

@test "log.msg handles case-insensitive level (debug -> DEBUG)" {
  SCRIPT_DEBUG=1 run --separate-stderr log.msg "debug" "Case test"
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*DEBUG.*Case\ test ]]
  [[ "${output}" == "" ]]
}

@test "log.msg handles case-insensitive level (Info -> INFO)" {
  run --separate-stderr log.msg "Info" "Case test for info"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*Case\ test\ for\ info ]]
  [[ "${stderr}" == "" ]]
}

@test "log.msg handles empty message gracefully" {
  run --separate-stderr log.msg "info"
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "" ]]
  [[ "${stderr}" == "" ]]
}

# --- Tests for log.set_level function ---

@test "log.set_level sets valid log level" {
  run bash -c 'source ./common_lib.bash && log.set_level DEBUG && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

@test "log.set_level rejects invalid log level" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level INVALID'
  [[ "${status}" -eq 1 ]]
  [[ "${stderr}" =~ .*FATAL.*Invalid\ log\ level:\ INVALID ]]
}

@test "log.set_level is case insensitive" {
  run bash -c 'source ./common_lib.bash && log.set_level debug && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

# --- Tests for log.trace function ---

@test "log.trace convenience function works" {
  run --separate-stderr bash -c 'source ./common_lib.bash && log.set_level TRACE && log.trace "This is a trace message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*TRACE.*This\ is\ a\ trace\ message ]]
  [[ "${output}" == "" ]]
}
