# `env2vars` Dynamic CI metadata collection and normalization

## Problem description

We send data to reporting for visualization and analysis

We send 2 main "chunks" of data in each event:

1. **Tests** answer questions such as the following:
   1. which test suite(s) ran, with which results, timings and errors, and for each suite?
      1. which test cases ran and with which results, timings and errors?
2. **metadata** answers the questions like
   1. what triggered the run?
   2. where did it run?
   3. what version(s) of which products were tested?
   4. what types of tests ran?
   5. who is the author of the changes?
   6. where is the code?
   7. which team supports issues for this code?

### Tests

The tests' reports are unified by JUnit format, so using various systems' outputs keeps the tests in the same structure.

### Metadata

However, the metadata comes from the CI system. And there are many of them

#### Abundance

Currently, only one group I am working at uses the following CI system types interchangeably:

* [Distributed CI](https://distributed-ci.io) (a.k.a. DCI)
* [GitLab](https://gitlab.com)
* [GitHub](https://github.com)
* [Jenkins](https://www.jenkins.io)
* [Prow](https://prow.ci.openshift.org)

Even though the intent is to reduce the number of CI system types, the tools tend to:

* change over the time without backward compatibility
* new tools come up
* the migrations efforts are prioritized lower than other efforts

#### Disparity between CI systems metadata

Each CI system generates metadata in its own specific manner.
There are 2 most common methods to communicate current runtime dynamic metadata, either by exposing:

1. an extensive set of environment variables
2. single environment variable, pointing at a file with structured JSON payload
3. both

Still, each CI system has its own considerations, terminology and this data is kept in different structures/environment variables.

## Solution Overview

In short, the user may be limited by organizational constraints with <sup>[*](#our-group)</sup>:

1. not enough permissions to allow quick reporting-side rollout cadence depending on organizational regulations/policies.
2. a healthy desire to generate CI-invariant queries in the dashboards.

Ergo, the minimal external dependency path is to normalize the data structure pre-ingestion.

### Implementation

For each CI system we create:

* `env2vars` maps environment variables to event metadata through `trs_vars_dict`.
* `trs_vars_dict` contains the data used to directly populate `event.metadata`.

The structure of the event is defined in [this file](event.md).
It usually has the following information under `event.metadata[]`:

| event coordinates(*) | `trs_vars_dict` keys  | example key            | key coordinates         |
| -------------------- | --------------------- | ---------------------- | ----------------------- |
| `.ci[]`              | `ci_*`                | `ci_url`               | `.ci.url`               |
| `.ci.runner[]`       | `ci_runner_*`         | `ci_runner_name`       | `.ci.runner.name`       |
| `.pipeline[]`        | `pipeline_*`          | `pipeline_id`          | `.pipeline.id`          |
| `.job[]`             | `job_*`               | `job_url`              | `.job.url`              |
| `.source[]`          | `source_*`            | `source_sha`           | `.source.sha`           |
| `.source.change[]`   | `source_change_*`     | `source_change_author` | `.source.change.author` |
| `.product[]`         | `product_*`           | `product_name`         | `.product.name`         |

(*) - written using `jq` notation

In `env2vars` we map this metadata into event's `metadata`.
This is done in these stages:

1. During the development, `env2vars` is populated by a list of key->var dictionaries defining keys from environment variables.
2. During runtime the role iterates over `env2vars` keys, and assigns them in the transition dictionary `trs_vars_dict`
3. Next, it repeats over the populated `trs_vars_dict` properly assigning its keys under `metadata` of the event
4. The translation of `trs_vars_dict` keys into actual event's `metadata` keys is relatively static

This approach allows:

* better readability because of less code duplications and significant similarity between CI systems
* the only exception is `DCI`: because it is not actually running anything, just storing already passed process information

So, `trs_vars_dict` is a transition variable to construct `metadata` part of the event being reported.

1. For every supported CI type, we should have proper `vars/env2vars/{{ trs_ci_type }}.yml` in the role.
2. The list `env2vars` is used to update `trs_vars_dict` keys.
3. `trs_vars_dict` keys are used to populate actual `.event.metadata[]` attributes
4. Metadata maintenance is thus reduced to generating the list, and sometimes adjusting which `trs_vars_dict` keys
   populate which `event.metadata[]` attributes.

The following types are supported:

| Type   | Constraints              |
| ------ | ------------------------ |
| `list` | flat list of strings (*) |
| `dict` | flat, see (**)           |
| `int`  | integer                  |
| `bool` | boolean                  |
| `str`  | string, default          |

### (*)

Assumes a list of strings, given the data is formatted as follows:

```text
'<elm><elmsep><elm><elmsep>....<elmsep><elm>'
```

| token      | meaning           |
| ---------- | ----------------- |
| `<elm>`    | element           |
| `<elmsep>` | element separator |

Parsed as a list of **strings**, into:

```yaml
${key}: # actual value of `key` in `env2vars` is used
  - '<elm>'
  ...
  - '<elm>'
```

### (**)

Assumes flat dicts, given the data is formatted as follows:

```text
'<k><kvsep><v><elmsep><k><kvsep><v>...<elmsep><k><kvsep><v>'
```

| token      | meaning             |
| ---------- | ------------------- |
| `<elmsep>` | elements separator  |
| `<k>`      | key                 |
| `<v>`      | value               |
| `<kvsep>`  | key/value separator |

Parsed as a **flat** dict of into:

```yaml
${key}: # actual value of `key` in `env2vars` is used
  '<k>': '<v>'
  '<k>': '<v>'
  ...
  '<k>': '<v>'

```

## Defining variables

### Where to define them

1. Identify the file based on the CI you know

They need to be added in `env2vars` list in a file `vars/<trs_ci_type>.yml`
That is, if the `trs_ci_type` is `github`, the file you edit is: `vars/env2vars/github.yml`

   1. If the file is not present, create it

## How to define each type

### String (`str`)

#### YAML structure

```yaml
---
env2vars:
  - key: my_key
    var: MY_ENV_VAR
    var_type: str
```

##### Examples

| Environment                | `vars_dict` as dict  |
| -------------------------- | -------------------- |
| `export MY_ENV_VAR="kuku"` | `{"my_key": "kuku"}` |

#### Comments

This type is the **default** type, no need to specify it

### List (`list`)

#### YAML structure

```yaml
env2vars:
  - key: my_lst_key
    var: MY_ENV_LIST_VAR
    var_type: list
    splitter:
      - '/'
```

**NOTE:** default splitter does not need to be specified

##### Examples

| Environment | `vars_dict` as dict |
| ----------- | ------------------- |
| `MY_ENV_LIST_VAR="kuku, lala/ blabla"` | `{"my_lst_key": ["kuku, lala", " blabla"]}` |
| `MY_ENV_LIST_VAR="path/to/some"` | `{"my_lst_key": ["path", "to", "some"]}` |

**NOTE:** spaces are not stripped.

### Dictionary (`dict`)

#### YAML structure

```yaml
---
env2vars:
  - key: my_dict_key
    var: MY_ENV_DICT_VAR
    var_type: dict
    splitter:
      - ' '
      - ':'
```

##### Examples

| Environment | `vars_dict` contents |
| ----------- | -------------------- |
| `MY_ENV_DICT_VAR="os:linux arch:x86_64 arch:amd64"` | `{"my_dict_key": {"os": "linux", "arch": ["x86_64", "amd64"]}}` |

#### Comments

The above splitters are the **default**, so they can be omitted.
Other interesting combinations of splitters are possible

### Integer (`int`)

#### YAML structure

```yaml
env2vars:
  - key: my_number
    var: MY_ENV_NUMBER
    var_type: int
```

##### Examples

| Environment | `vars_dict` as dict |
| ----------- | ------------------- |
| `MY_ENV_VAR="34213"` | `{"my_number": 34213}` |

### Boolean (`bool`)

#### YAML structure

```yaml
---
env2vars:
  - key: my_bool
    var: MY_BOOL_TRUTH
    var_type: bool

```

##### Examples

| Environment              | `vars_dict` as dict  |
| ------------------------ | -------------------- |
| `MY_BOOL_TRUTH="false"`  | `{"my_bool": false}` |
| `MY_BOOL_TRUTH="1"`      | `{"my_bool": true}`  |
| `MY_BOOL_TRUTH="0"`      | `{"my_bool": false}` |
| `MY_BOOL_TRUTH="false"`  | `{"my_bool": false}` |
| `MY_BOOL_TRUTH="string"` | `{"my_bool": true}`  |

## Constraints

<sup>*</sup><a name="our-group"></a> Our group constraints:

* We do not have full control of our reporting systems because we are only users.
* So we cannot rely on our capability to post-ingest processing, which is too much overhead.
