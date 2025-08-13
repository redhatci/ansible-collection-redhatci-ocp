# Hack / maintenance scripts for internal use only

This directory is intended for maintainers/developers

## bash library: `hack/base.bash`

### Features by example

#### Assumptions

1. The script is going to be under `hack/`

#### Integrating

**i. load the lib somewhere at the top of the script:**

```bash
# --- loading the library ---
TOPDIR="${TOPDIR:-"$(git rev-parse --show-toplevel || true)"}"
source "${TOPDIR}/hack/base.bash"
# --- end loading the library ---
```

Now you can call its functions

**ii. initialize good `FIND`, `GREP`, `SED` values:**

```bash
utils.tools_setup
```

### 0. Usage

### 1. logging

#### Default behavior

```bash
host:ocp user$ source ./hack/base.bash
host:ocp user$ echo "LOG_LEVEL: '${LOG_LEVEL}'"
LOG_LEVEL: 'INFO'
host:ocp user$ log.info "The info message"   # stdout [[ "${LEVELS_MAP[INFO]}" -ge "${LEVELS_MAP["${LOG_LEVEL}"]}" ]]
Thu Jul 24 14:07:01 UTC 2025 - INFO - The info message
host:ocp user$ log.debug "The debug message" # stderr [[ "${LEVELS_MAP[DEBUG]}" -ge "${LEVELS_MAP["${LOG_LEVEL}"]}" ]]
host:ocp user$ log.warning "The my warning"  # stderr [[ "${LEVELS_MAP[WARNING]}" -ge "${LEVELS_MAP["${LOG_LEVEL}"]}" ]]
Thu Jul 24 14:07:01 UTC 2025 - WARNING - The my warning
host:ocp user$ log.fatal "The fatality of life" # stderr
Thu Jul 24 14:07:01 UTC 2025 - FATAL - The fatality of life
```

#### Controlling the log level

| Option # | Preference | Function        | Variable       | Control           | Comments                               |
| -------- | ---------- | --------------- | -------------- | ----------------- | -------------------------------------- |
| `i.`     | Default    | N/A             | `SCRIPT_DEBUG` | +Good             | `0: INFO`, `1: DEBUG`,`2: TRACE`       |
| `ii.`    | Proper     | `log.set_level` | `LOG_LEVEL`    | +Full,+Safeguards | [`LEVELS_MAP`](hack/base.bash#L486)    |
| `iii.`   | Hackish    | None            | `LOG_LEVEL`    | +Full,-Safeguards | Unsafe                                 |

##### Examples

i. This is the simple default:

```bash
host:ocp user$ # using SCRIPT_DEBUG
host:ocp user$ for value in {0..2}; do
    bash -c 'SCRIPT_DEBUG="'${value}'"; source ./hack/base.bash; echo "LOG_LEVEL: ${LOG_LEVEL}"'
done
LOG_LEVEL: INFO
LOG_LEVEL: DEBUG
LOG_LEVEL: TRACE
host:ocp user$
host:ocp user$ source ./hack/base.bash
host:ocp user$ log.set_level WARNING
host:ocp user$ log.info "info not printing"
host:ocp user$ log.warning "warning printing"
Thu Jul 24 14:40:43 UTC 2025 - WARNING - warning printing
host:ocp user$ log.error "errors printing"
Thu Jul 24 14:41:08 UTC 2025 - ERROR - errors printing
host:ocp user$ log.fatal "fatal printing"
Thu Jul 24 14:41:17 UTC 2025 - FATAL - fatal printing
host:ocp user$
host:ocp user$ for value in DEBUG WARNING INFO; do
  bash -c 'export LOG_LEVEL="'${value}'"; source ./hack/base.bash; echo "LOG_LEVEL: ${LOG_LEVEL}"; log.info "super informative message"'
done
LOG_LEVEL: DEBUG
LOG_LEVEL: WARNING
LOG_LEVEL: INFO
host:ocp user$ source ./hack/base.bash
host:ocp user$ for value in DBG WARN NFO; do LOG_LEVEL="${value}"; log.debug "Hello"; echo "rc: $?"; done
Mon Jul 28 23:17:06 UTC 2025 - FATAL - LOG_LEVEL='DBG' is invalid. Valid values are: TRACE, ERROR, INFO, WARNING, FATAL, DEBUG
rc: 1
Mon Jul 28 23:17:06 UTC 2025 - FATAL - LOG_LEVEL='WARN' is invalid. Valid values are: TRACE, ERROR, INFO, WARNING, FATAL, DEBUG
rc: 1
Mon Jul 28 23:17:06 UTC 2025 - FATAL - LOG_LEVEL='NFO' is invalid. Valid values are: TRACE, ERROR, INFO, WARNING, FATAL, DEBUG
rc: 1
makovgan-mac:ocp makovgan$ echo $?
1

```

### 2. Utilities

```bash
host:ocp user$ source ./hack/base.bash
host:ocp user$ x=("a" "b" "c d" "e")
host:ocp user$ # txt.join_by joins array with "joiner" string
host:ocp user$ txt.join_by '+' "${x[@]}"
a+b+c d+e
host:ocp user$ # for example we can print out a list:
host:ocp user$ echo "list: ['$(txt.join_by "', '" "${x[@]}")']"
list: ['a', 'b', 'c d', 'e']
host:ocp user$ # txt.contains_element <item> <items> (checks whether item is in items)
host:ocp user$ txt.contains_element "c d" "${x[@]}"
host:ocp user$ echo $?
0
host:ocp user$ # 0 means true
host:ocp user$ txt.contains_element "g" "${x[@]}"
host:ocp user$ echo $?
1
host:ocp user$ # 1 means false
host:ocp user$ # utils.tools_setup sets up FIND, SED and GREP env variables to point to the relevant tools for the OS
host:ocp user$ utils.tools_setup # this function sets up FIND, SED and GREP variables to point to the relevant ones for the OS
host:ocp user$ app.run 0 true # 1st argument is expected good return code
host:ocp user$ app.run 1 true # will exit
logout
host:ocp user$ # if this is set: DO_NOT_EXIT=1 log.die() returns instead of exit, causing app.run() to stay in the shell
host:ocp user$ # DO_NOT_EXIT=1 allows failing run_cmd to return instead of exit
host:ocp user$ # don't forget to unset it:
host:ocp user$ source hack/base.bash
host:ocp user$ app.run 0 true
host:ocp user$ echo $?
0
host:ocp user$ DO_NOT_EXIT=1 # without this variable, this shell session will terminate upon any failure
host:ocp user$ app.run 0 false
Thu Jul 24 15:49:40 UTC 2025 - FATAL - The command 'false' returned unexpected rc=1. [EXPECTED: 0]
host:ocp user$ echo $?
1
host:ocp user$ DO_NOT_EXIT=0 # here the failure causes the session to terminate
host:ocp user$ app.run 0 false
Thu Jul 24 15:49:40 UTC 2025 - FATAL - The command 'false' returned unexpected rc=1. [EXPECTED: 0]
logout
```

### 3. More details

You are most welcome to read these files:

- code: [`hack/base.bash`](hack/base.bash)
- tests: [`hack/test/test_base.bats`](hack/test/test_base.bats)
