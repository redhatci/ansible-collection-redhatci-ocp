#!/usr/bin/env bats
# shellcheck disable=SC2154
bats_require_minimum_version 1.5.0

# Note: We don't use 'load' because it causes initialization issues
# Instead, each test explicitly sources the library as needed

# --- Unit Tests for app.run ---

# debug function to print variables
print_vars() {
  {
    echo "output:='${output}'"
    echo "stdout:='${stdout}'"
    echo "stderr:='${stderr}'"
    echo "status:='${status}'"
  } >&3
}

@test "test app.run with expected_rc=0" {
  expected="Hello, world."
  run bash -c "source hack/base.bash && app.run 0 echo '${expected}'"
  # print_vars
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "${expected}" ]]
}

@test "test app.run with expected_rc=1" {
  run bash -c "source hack/base.bash && app.run 1 false"
  [[ "${status}" -eq 1 ]]
  [[ "${output}" == "" ]]
}

@test "test app.run with expected_rc=1 and DO_NOT_EXIT=1" {
  run --separate-stderr bash -c "source hack/base.bash && export DO_NOT_EXIT=1 && app.run 0 false"
  [[ "${status}" -eq 1 ]]
  [[ "${output}" == "" ]]
  [[ "${stderr}" =~ .*FATAL.* ]]
}

@test "test app.run with DO_NOT_EXIT=0 (default) - function calls exit" {
  # When DO_NOT_EXIT=0 (default), log.die should call exit() and terminate the process
  run --separate-stderr bash -c "source hack/base.bash && unset DO_NOT_EXIT && app.run 0 false"
  # The bash process should exit with the error code from log.die
  [[ "${status}" -eq 1 ]]
  [[ "${output}" == "" ]]
  [[ "${stderr}" =~ .*FATAL.* ]]
}

@test "test app.run with DO_NOT_EXIT=1 - function returns without exit" {
  # When DO_NOT_EXIT=1, log.die should return instead of exit, allowing script to continue
  run --separate-stderr bash -c "
    source hack/base.bash
    export DO_NOT_EXIT=1
    app.run 0 false
    echo 'Script continued after error'
  "
  # The script should continue and print the message
  [[ "${status}" -eq 0 ]]  # Overall script succeeds because it continues
  [[ "${output}" == "Script continued after error" ]]
  [[ "${stderr}" =~ .*FATAL.* ]]
}

@test "test log.die directly with DO_NOT_EXIT=0 - should exit process" {
  # Test log.die directly to ensure it exits when DO_NOT_EXIT=0
  run --separate-stderr bash -c "
    source hack/base.bash
    export DO_NOT_EXIT=0
    log.die 42 'Test error message'
    echo 'This should never print'
  "
  # Process should exit with code 42, never reaching the echo
  [[ "${status}" -eq 42 ]]
  [[ "${output}" == "" ]]
  [[ "${stderr}" =~ .*FATAL.*Test\ error\ message ]]
}

@test "test log.die directly with DO_NOT_EXIT=1 - should return" {
  # Test log.die directly to ensure it returns when DO_NOT_EXIT=1
  run --separate-stderr bash -c "
    source hack/base.bash
    export DO_NOT_EXIT=1
    if log.die 42 'Test error message'; then
      echo 'log.die returned true (should not happen)'
    else
      echo 'log.die returned false with code: \$?'
    fi
    echo 'Script continued after log.die'
  "
  # Script should continue after log.die returns
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*Script\ continued\ after\ log\.die ]]
  [[ "${stderr}" =~ .*FATAL.*Test\ error\ message ]]
}

# --- Unit Tests for utils.tools_setup ---

tools_setup_and_print_vars() {
  local rc os
  local -a \
    items
  os="${1}"
  shift 1
  items=("${@}")

  # Redirect log output to avoid interfering with variable output
  utils.tools_setup "${os}" 2>/dev/null
  rc=$?
  for item in "${items[@]}"; do
    echo "${item}='$(eval echo "\${${item}}" || true)'"
  done
  return "${rc}"
}

@test "test utils.tools_setup('Linux') assigning FIND=find, GREP=grep, SED=sed" {
  OS="Linux"
  FIND="find"
  GREP="grep"
  SED="sed"
  declare -A expected
  expected[FIND]="find"
  expected[GREP]="grep"
  expected[SED]="sed"
  run bash -c "
    source hack/base.bash
    $(declare -f tools_setup_and_print_vars)
    tools_setup_and_print_vars '${OS}' 'FIND' 'GREP' 'SED'
  "
  [[ "${status}" -eq 0 ]]
  eval "${output}"
  [[ "${FIND}" = "${expected[FIND]}" ]]
  [[ "${GREP}" = "${expected[GREP]}" ]]
  [[ "${SED}" = "${expected[SED]}" ]]
}

@test "test utils.tools_setup('Darwin') assigning FIND=gfind, GREP=ggrep, SED=gsed" {
  OS="Darwin"
  FIND="find"
  GREP="grep"
  SED="sed"
  declare -A expected
  expected[FIND]="gfind"
  expected[GREP]="ggrep"
  expected[SED]="gsed"
  run bash -c "
    source hack/base.bash
    $(declare -f tools_setup_and_print_vars)
    tools_setup_and_print_vars '${OS}' 'FIND' 'GREP' 'SED'
  "
  [[ "${status}" -eq 0 ]]
  eval "${output}"
  [[ "${FIND}" = "${expected[FIND]}" ]]
  [[ "${GREP}" = "${expected[GREP]}" ]]
  [[ "${SED}" = "${expected[SED]}" ]]
}

@test "test utils.tools_setup on Unsupported OS to fail" {
  # Test tools_setup directly since we expect it to fail and need the stderr
  run --separate-stderr bash -c "
    source hack/base.bash
    utils.tools_setup 'OpenBSD'
  "
  [[ "${status}" -eq 1 ]]
  [[ "${stderr}" =~ .*Unsupported\ OS:\ OpenBSD ]]
}

# --- Unit Tests for log.msg basic functionality ---

@test "log.msg INFO prints to stdout" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg info 'This is an info message'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*This\ is\ an\ info\ message ]]
}

@test "log.msg ERROR prints to stderr" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg error 'This is an error message'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*This\ is\ an\ error\ message ]]
  [[ "${output}" == "" ]]
}

@test "log.msg WARNING prints to stderr" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg warning 'This is a warning message'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*This\ is\ a\ warning\ message ]]
  [[ "${output}" == "" ]]
}

@test "log.msg FATAL prints to stderr" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg fatal 'This is a fatal message'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*FATAL.*This\ is\ a\ fatal\ message ]]
  [[ "${output}" == "" ]]
}

# --- Tests for SCRIPT_DEBUG behavior (when LOG_LEVEL is not manually overridden) ---

@test "SCRIPT_DEBUG=0 sets LOG_LEVEL=INFO" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=0 source hack/base.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=INFO ]]
}

@test "SCRIPT_DEBUG=1 sets LOG_LEVEL=DEBUG" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=1 source hack/base.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

@test "SCRIPT_DEBUG=2 sets LOG_LEVEL=TRACE" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=2 source hack/base.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=TRACE ]]
}

@test "SCRIPT_DEBUG=invalid sets LOG_LEVEL=INFO (default)" {
  run bash -c 'unset LOG_LEVEL && SCRIPT_DEBUG=99 source hack/base.bash && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=INFO ]]
}

# --- Tests for level filtering (message level vs LOG_LEVEL comparisons) ---

@test "TRACE message prints when LOG_LEVEL=TRACE" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level TRACE && log.msg trace "Trace message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*TRACE.*Trace\ message ]]
}

@test "TRACE message filtered when LOG_LEVEL=DEBUG" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level DEBUG && log.msg trace "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "DEBUG message prints when LOG_LEVEL=DEBUG" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level DEBUG && log.msg debug "Debug message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*DEBUG.*Debug\ message ]]
}

@test "DEBUG message filtered when LOG_LEVEL=INFO" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level INFO && log.msg debug "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "INFO message prints when LOG_LEVEL=INFO" {
  run bash -c 'source hack/base.bash && log.set_level INFO && log.msg info "Info message"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*Info\ message ]]
}

@test "INFO message filtered when LOG_LEVEL=WARNING" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level WARNING && log.msg info "Should not appear"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" == "" ]]
  [[ "${output}" == "" ]]
}

@test "WARNING message prints when LOG_LEVEL=WARNING" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level WARNING && log.msg warning "Warning message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*Warning\ message ]]
}

@test "WARNING message prints when LOG_LEVEL=INFO (higher level always prints)" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level INFO && log.msg warning "Warning message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*WARNING.*Warning\ message ]]
}

@test "ERROR message prints when LOG_LEVEL=ERROR" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level ERROR && log.msg error "Error message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Error\ message ]]
}

@test "ERROR message prints when LOG_LEVEL=INFO (higher level always prints)" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level INFO && log.msg error "Error message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Error\ message ]]
}

@test "FATAL message always prints regardless of LOG_LEVEL" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level FATAL && log.msg fatal "Fatal message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*FATAL.*Fatal\ message ]]
}

@test "log.msg handles multiple message arguments" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg error 'Multiple' 'message' 'arguments'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*ERROR.*Multiple\ message\ arguments ]]
}

@test "log.msg handles case-insensitive level (debug -> DEBUG)" {
  run --separate-stderr bash -c "
    export SCRIPT_DEBUG=1
    source hack/base.bash
    log.msg debug 'Case test'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*DEBUG.*Case\ test ]]
  [[ "${output}" == "" ]]
}

@test "log.msg handles case-insensitive level (Info -> INFO)" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg Info 'Case test for info'
  "
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ .*INFO.*Case\ test\ for\ info ]]
  [[ "${stderr}" == "" ]]
}

@test "log.msg handles empty message gracefully" {
  run --separate-stderr bash -c "
    source hack/base.bash
    log.msg info
  "
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "" ]]
  [[ "${stderr}" == "" ]]
}

# --- Tests for log.set_level function ---

@test "log.set_level sets valid log level" {
  run bash -c 'source hack/base.bash && log.set_level DEBUG && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

@test "log.set_level rejects invalid log level" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level INVALID'
  [[ "${status}" -eq 1 ]]
  [[ "${stderr}" =~ .*FATAL.*Invalid\ log\ level:.*INVALID ]]
}

@test "log.set_level is case insensitive" {
  run bash -c 'source hack/base.bash && log.set_level debug && echo "LOG_LEVEL=$LOG_LEVEL"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ LOG_LEVEL=DEBUG ]]
}

# --- Tests for log.trace function ---

@test "log.trace convenience function works" {
  run --separate-stderr bash -c 'source hack/base.bash && log.set_level TRACE && log.trace "This is a trace message"'
  [[ "${status}" -eq 0 ]]
  [[ "${stderr}" =~ .*TRACE.*This\ is\ a\ trace\ message ]]
  [[ "${output}" == "" ]]
}

# --- Tests for DO_NOT_EXIT=1 edge cases ---

@test "log.set_level rejects invalid log level with DO_NOT_EXIT=1 - should return error code" {
  run --separate-stderr bash -c '
    export DO_NOT_EXIT=1
    source hack/base.bash
    log.set_level INVALID
    echo "Exit code: $?"
  '
  [[ "${status}" -eq 0 ]]              # Overall script succeeds
  [[ "${output}" =~ Exit\ code:\ 1 ]]  # But log.set_level returned 1
  [[ "${stderr}" =~ .*FATAL.*Invalid\ log\ level:.*INVALID ]]
}

@test "utils.tools_setup with unsupported OS and DO_NOT_EXIT=1 - should return error code" {
  run --separate-stderr bash -c '
    export DO_NOT_EXIT=1
    source hack/base.bash
    utils.tools_setup OpenBSD
    echo "Exit code: $?"
  '
  [[ "${status}" -eq 0 ]]              # Overall script succeeds
  [[ "${output}" =~ Exit\ code:\ 1 ]]  # But tools_setup returned 1
  [[ "${stderr}" =~ .*FATAL.*Unsupported\ OS:\ OpenBSD ]]
}

@test "log.init with invalid LOG_LEVEL and DO_NOT_EXIT=1 - should return error code" {
  run --separate-stderr bash -c '
    export DO_NOT_EXIT=1
    export LOG_LEVEL=INVALID
    source hack/base.bash
    echo "Exit code: $?"
  '
  [[ "${status}" -eq 0 ]]              # Overall script succeeds
  [[ "${output}" =~ Exit\ code:\ 1 ]]  # But log.init returned 1
  [[ "${stderr}" =~ .*FATAL.*LOG_LEVEL=.*INVALID.*is\ invalid ]]
}

@test "util.validate_bash succeeds on modern bash versions" {
  run bash -c 'source hack/base.bash && util.validate_bash && echo "Validation passed"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" =~ Validation\ passed ]]
}

@test "txt.join_by works with empty array" {
  run bash -c 'source hack/base.bash && txt.join_by ","'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "" ]]
}

@test "txt.join_by works with single element array" {
  run bash -c 'source hack/base.bash && txt.join_by "," "a"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "a" ]]
}

@test "txt.join_by works with multiple elements" {
  run bash -c 'source hack/base.bash && txt.join_by "," "a" "b" "c"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "a,b,c" ]]
}

@test "txt.join_by works with empty separator" {
  run bash -c 'source hack/base.bash && txt.join_by "" "a" "b" "c"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "abc" ]]
}

@test "txt.join_by works with formatting separator" {
  run bash -c 'source hack/base.bash && txt.join_by "%,%" "a" "b" "c"'
  [[ "${status}" -eq 0 ]]
  [[ "${output}" == "a%,%b%,%c" ]]
}
