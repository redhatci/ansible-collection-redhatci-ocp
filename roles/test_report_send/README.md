<!-- DOCSIBLE START -->

# 📃 Role overview

## test_report_send

```
Role belongs to redhatci/ocp
Namespace - redhatci
Collection - ocp
Version - 0.23.0
Repository - https://github.com/redhatci/ansible-collection-redhatci-ocp
```

Description: Push data file to collector


| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 16/12/2024 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main 
**Description**: This is the main entrypoint for the `redhatci.ocp.test_report_send` role. It sends data to the collector, currently only splunk is supported.



  - **trs_collector_url**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: The URL of collector server (Splunk)

  
  
  

  - **trs_collector_auth_token**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: This is the collector auth token string as for basic http auth

  
  
  

  - **trs_collector_target**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: Target/Channel/Topic/Id/ of the collector

  
  
  

  - **trs_report_file_path**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: File to send. it is assumed to have `metadata.json` nearby or up in the filesystem.

  
  
  

  - **trs_reports_path_patterns**
    - **Required**: False
    - **Type**: list
    - **Default**: ['*.json']
    - **Description**: The list of name regex to match only relevant XML files for consolidation

  
  
  

  - **global_partner**
    - **Required**: False
    - **Type**: str
    - **Default**: 
    - **Description**: Whether this is a partner

  
  
  



</details>


### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [trs_reports_path_patterns](defaults/main.yml#L10)   | list   | `['*.json']` |    n/a  |  n/a |





### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Use the first file (even if the result isn't 1 file) | ansible.builtin.set_fact | True |
| Read content from test data JSON file | ansible.builtin.slurp | False |
| Decode JSON content for test file | ansible.builtin.set_fact | False |
| Set default empty metadata file name | ansible.builtin.set_fact | False |
| Find metadata location | ansible.builtin.shell | False |
| Extract metadata file name | ansible.builtin.set_fact | True |
| Read content from metadata JSON file | ansible.builtin.slurp | True |
| Setup content for metadata file | ansible.builtin.set_fact | False |
| Decode JSON content for metadata file | ansible.builtin.set_fact | True |
| Create event data attributes | ansible.builtin.set_fact | False |
| Setup timestamps broken down to int/float parts | ansible.builtin.set_fact | False |
| Setup timestamps as floats | ansible.builtin.set_fact | False |
| Set event time if we have job_time | ansible.builtin.set_fact | True |
| Update event data timestamps to be in epoch ms format | ansible.builtin.set_fact | False |
| Print event data | ansible.builtin.debug | False |
| Combine additional attributes into the data | ansible.builtin.set_fact | False |
| Print payload data | ansible.builtin.debug | False |
| Send data to Splunk HEC | ansible.builtin.uri | False |




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