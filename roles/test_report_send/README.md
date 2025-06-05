<!-- DOCSIBLE START -->

# 📃 Role overview

## test_report_send

Description: Push data file to collector

<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: This is the main entrypoint for the role `redhatci.ocp.test_report_send`.
The role constructs a single event made of:

* tests report data: `trs_report_path`
* runtime metadata, either:
  * `trs_metadata_path`
  * CI specific metadata collected from environment variables
This event is sent to the collector (currently only splunk is supported).

  * **trs_report_path**
    * **Required**: False
    * **Type**: str
    * **Default**: none
    * **Description**: Test report JSON file to send.
Merged into the event under 'test' attribute.
For full report syntax see (TBD).

  * **trs_metadata_path**
    * **Required**: False
    * **Type**: str
    * **Default**:
    * **Description**: Event metadata JSON file to send.
Merged into the event 'metadata' attribute.
Useful to mark special datasets during development.
If set to be empty or the file is missing, it is ignored.

  * **trs_collector_url**
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: The URL of collector server (Splunk).

  * **trs_collector_auth_token**
    * **Required**: False
    * **Type**: str
    * **Default**: none
    * **Description**: Collector auth token string for Bearer Token HTTP Authentication.

  * **trs_collector_target**
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: Collector Target/Channel/Topic/Id

  * **trs_collector**
    * **Required**: False
    * **Type**: str
    * **Default**: splunk
    * **Description**: Collector type (currently only `splunk` is supported).

  * **trs_collectors_supported**
    * **Required**: False
    * **Type**: list
    * **Default**: ['splunk']
    * **Description**: Supported collectors types list.

  * **trs_ci_systems_supported**
    * **Required**: False
    * **Type**: list
    * **Default**: ['dci', 'jenkins', 'prow']
    * **Description**: Supported CI systems list.

  * **trs_collector_auth_headers**
    * **Required**: False
    * **Type**: dict
    * **Default**: {}
    * **Description**: Collector request HTTP headers for HTTP Authentication.

  * **trs_ci_system_autodetect**
    * **Required**: False
    * **Type**: bool
    * **Default**: False
    * **Description**: Skip auto-detection of CI system (mainly mor dev).

</details>

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [trs_report_path](defaults/main.yml#L5)   | str   | `` |    n/a  |  n/a |
| [trs_metadata_path](defaults/main.yml#L6)   | str   | `` |    n/a  |  n/a |
| [trs_collector](defaults/main.yml#L7)   | str   | `splunk` |    n/a  |  n/a |
| [trs_ci_systems_supported](defaults/main.yml#L8)   | list   | `['jenkins', 'dci', 'prow']` |    n/a  |  n/a |
| [trs_collectors_supported](defaults/main.yml#L12)   | list   | `['splunk']` |    n/a  |  n/a |
| [trs_ci_system](defaults/main.yml#L15)   | str   | `unknown` |    n/a  |  n/a |
| [trs_do_send](defaults/main.yml#L16)   | bool   | `True` |    n/a  |  n/a |
| [trs_ci_system_autodetect](defaults/main.yml#L17)   | bool   | `False` |    n/a  |  n/a |

### Tasks

#### File: tasks/ci.detect.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Define default CI system name | ansible.builtin.set_fact | False |
| Set DCI as trs_ci_system | ansible.builtin.set_fact | True |
| Set Prow as trs_ci_system | ansible.builtin.set_fact | True |
| Set Jenkins as trs_ci_system | ansible.builtin.set_fact | True |
| Set GitHub as trs_ci_system | ansible.builtin.set_fact | True |
| Set GitLab as trs_ci_system | ansible.builtin.set_fact | True |

#### File: tasks/metadata.detect.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Detect CI system | ansible.builtin.include_tasks | True |
| Initialize metadata if empty | ansible.builtin.set_fact | False |
| Detect dynamic metadata | ansible.builtin.include_tasks | False |
| Update metadata | ansible.builtin.set_fact | False |
| Update trs_collector_source for {{ trs_ci_system }} | ansible.builtin.set_fact | True |

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Update trs_report_path if not passed | ansible.builtin.set_fact | True |
| Validate all required variables are defined | ansible.builtin.assert | False |
| Collect trs_report_path file stat | ansible.builtin.stat | False |
| Ensure trs_report_path file exists | ansible.builtin.assert | False |
| Collect trs_metadata_path file stat | ansible.builtin.stat | True |
| Read content of metadata JSON file | ansible.builtin.slurp | True |
| Setup content for metadata file | ansible.builtin.set_fact | False |
| Decode JSON content for metadata file | ansible.builtin.set_fact | True |
| Detect Metadata from the env | ansible.builtin.include_tasks | False |
| Send trs_data_event to collector {{ trs_collector }} | ansible.builtin.include_tasks | False |

#### File: tasks/reporting/splunk.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Read content from test report JSON file | ansible.builtin.slurp | False |
| Decode JSON content of test report file | ansible.builtin.set_fact | False |
| Print current datetime | ansible.builtin.debug | False |
| Setup timestamps broken down to int/float parts for {{ trs_collector }} | ansible.builtin.set_fact | False |
| Setup timestamps as floats for reporting | ansible.builtin.set_fact | False |
| Update trs_collector_auth_headers with trs_collector_auth_token from the user for {{ trs_collector }} | ansible.builtin.set_fact | True |
| Update trs_collector_auth_headers with trs_event_channel from the user for {{ trs_collector }} | ansible.builtin.set_fact | True |
| Dynamically detect metadata when it is missing | ansible.builtin.include_tasks | True |
| Create event data attributes | ansible.builtin.set_fact | False |
| Print event data before timestamp corrections | ansible.builtin.debug | False |
| Combine additional attributes into the data at trs_collector_target for {{ trs_collector }} | ansible.builtin.set_fact | False |
| Print payload data | ansible.builtin.debug | False |
| Send data to {{ trs_collector }} | ansible.builtin.uri | True |

#### File: tasks/reporting/validations.splunk.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Validate collector connectivity var trs_collector_url is not empty | ansible.builtin.assert | False |
| Validate collector connectivity var trs_collector_auth_headers is not empty | ansible.builtin.assert | False |
| Validate collector var for splunk trs_collector_auth_headers has the required keys and values | ansible.builtin.assert | False |

#### File: tasks/metadata.detect/jenkins.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Set is_ci attribute | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.type for {{ trs_ci_system }} | ansible.builtin.set_fact | False |
| Update trs_ci_runtime.url for {{ trs_ci_system }} | ansible.builtin.set_fact | False |
| Update trs_ci_runtime.job for {{ trs_ci_system }} | ansible.builtin.set_fact | True |

#### File: tasks/metadata.detect/dci.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Set is_ci attribute | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.type for {{ trs_ci_system }} | ansible.builtin.set_fact | False |
| Update trs_ci_runtime.url for {{ trs_ci_system }} | ansible.builtin.set_fact | False |

#### File: tasks/metadata.detect/github.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Set is_ci attribute | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.type for {{ trs_ci_system }} | ansible.builtin.set_fact | False |
| Update trs_ci_runtime.url for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.pipeline for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.job for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.commit for {{ trs_ci_system }} | ansible.builtin.set_fact | True |

#### File: tasks/metadata.detect/unknown.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Unsupported CI system | ansible.builtin.debug | False |
| Fail the role | ansible.builtin.fail | False |

#### File: tasks/metadata.detect/gitlab.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Set is_ci attribute | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.type for {{ trs_ci_system }} | ansible.builtin.set_fact | False |
| Update trs_ci_runtime.url for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.pipeline for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.job for {{ trs_ci_system }} | ansible.builtin.set_fact | True |
| Update trs_ci_runtime.commit for {{ trs_ci_system }} | ansible.builtin.set_fact | True |

## Playbook

```yml
---
- hosts: localhost
  remote_user: root
  roles:
    - role: test_report_send
      

```

## Author Information

Max Kovgan, Cesare Placanica

#### License

Apache License, Version 2.0

#### Minimum Ansible Version

2.9

#### Platforms

No platforms specified.
<!-- DOCSIBLE END -->
