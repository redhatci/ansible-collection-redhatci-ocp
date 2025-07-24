# Hack / maintenance scripts for internal use only

This directory is intended for maintainers/developers

## bash library: `hack/common_lib.bash` info

### Features

### 1. logging

#### Default behavior

```bash
host:ocp user$ source ./hack/common_lib.bash
host:ocp user$ echo "LOG_LEVEL: '${LOG_LEVEL}'"
LOG_LEVEL: 'INFO'
host:ocp user$ log.info "The info message"      # printed to stdout (if "${LEVELS_MAP["INFO]}" >= "${LEVELS_MAP[${:%LOG_LEVEL}]}")
Thu Jul 24 14:07:01 UTC 2025 - INFO - The info message
host:ocp user$ log.debug "The debug message"    # printed to stderr (if "${LEVELS_MAP["DEBUG"] >= "${LEVELS_MAP[${LOG_LEVEL}]}")
host:ocp user$ log.warning "The my warning"     # printed to stderr (if "${LEVELS_MAP["WARNING"] >= "${LEVELS_MAP[${LOG_LEVEL}]}")
Thu Jul 24 14:07:01 UTC 2025 - WARNING - The my warning
host:ocp user$ log.fatal "The fatality of life" # is printed always to stderr (b/c always true: "${LEVELS_MAP[FATAL"] >= "${LEVELS_MAP[${LOG_LEVEL}]}")
Thu Jul 24 14:07:01 UTC 2025 - FATAL - The fatality of life
```

#### 1.1. Override using `SCRIPT_DEBUG`

```bash
host:ocp user$ for value in {0..2}; do
    bash -c 'SCRIPT_DEBUG="'${value}'" source ./hack/common_lib.bash; echo "LOG_LEVEL: ${LOG_LEVEL}"'
done
LOG_LEVEL: INFO
LOG_LEVEL: DEBUG
LOG_LEVEL: TRACE
host:ocp user$
```

#### 1.2. Override by setting of `LOG_LEVEL` variable

```bash
host:ocp user$ for value in DEBUG WARNING INFO; do
    bash -c 'LOG_LEVEL="'${value}'"; source ./hack/common_lib.bash; echo "LOG_LEVEL: ${LOG_LEVEL}"'
done
LOG_LEVEL: DEBUG
LOG_LEVEL: WARNING
LOG_LEVEL: INFO
host:ocp user$

```

#### 1.3. Override calling `log.set_level()`

```bash
host:ocp user$ source ./hack/common_lib.bash
host:ocp user$ log.set_level WARNING
host:ocp user$ log.info "info not printing"
host:ocp user$ log.warning "warning printing"
Thu Jul 24 14:40:43 UTC 2025 - WARNING - warning printing
host:ocp user$ log.error "errors printing"
Thu Jul 24 14:41:08 UTC 2025 - ERROR - errors printing
host:ocp user$ log.fatal "fatal printing"
Thu Jul 24 14:41:17 UTC 2025 - FATAL - fatal printing
host:ocp user$
```

### 2. Utilities

```bash
host:ocp user$ source ./hack/common_lib.bash
host:ocp user$ x=("a" "b" "c d" "e")
host:ocp user$ join_by '+' "${x[@]}"
a+b+c d+e
host:ocp user$ join_by '+'

host:ocp user$ contains_element "c d" "${x[@]}"
host:ocp user$ echo $?
0
host:ocp user$ contains_element "g" "${x[@]}"
host:ocp user$ echo $?
1
host:ocp user$ tools_setup # this function is setting SED and GREP variables to point to the relevant ones for the OS
host:ocp user$ run_cmd 0 true # 1st argument is expected good return code
host:ocp user$ run_cmd 1 true # will exit
host:ocp user$ # LIVE_FOREVER=1 allows failing run_cmd to return instead of exit
host:ocp user$ # don't forget to unset it:
host:ocp user$ # don't forget to unset it:
host:ocp user$ source hack/common_lib.bash
host:ocp user$ run_cmd 0 true
host:ocp user$ echo $?
0
host:ocp user$ LIVE_FOREVER=1
host:ocp user$ run_cmd 0 false
Thu Jul 24 15:49:40 UTC 2025 - FATAL - The command 'false' returned unexpected rc=1. [EXPECTED: 0]
host:ocp user$ echo $?
1
host:ocp user$ LIVE_FOREVER=0
host:ocp user$ # compare_versions "${left}" "${right}"
host:ocp user$ # prints -1 if "${left}" < "${right}", 0 if equal, 1 if "${left}" > "${right}" to stdout
host:ocp user$ left="1.0.2"; right="1.0.3"
host:ocp user$ source hack/common_lib.bash
host:ocp user$ left="1.0.2"; right="1.0.3"
host:ocp user$ compare_versions "${left}" "${right}" # left < right
-1
host:ocp user$ compare_versions "${right}" "${left}" # left > right
1
host:ocp user$ compare_versions "${right}" "${right}" # left == right
0

```
