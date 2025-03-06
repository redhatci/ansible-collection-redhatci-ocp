<!-- DOCSIBLE START -->

# 📃 Role overview

## junit2json



Description: Converts XML junit reports passed or in passed directory into single or fragmented JSON report file(s)







<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main 
**Description**: The resulting JSON file(s) are of the same structure for all the teams' and CI systems and used later to be sent to the data collection system.
This is the main entrypoint for the role `redhatci.ocp.junit2json`.
Converts XMLs into JSON, if variable `junit2json_do_merge` is `true`, multiple XMLs are merged into one XML file.
New filename(s) is(are) based on the old ones and stored in global variable `global_json_reports_list`.



  - **junit2json_input_reports_list**
    - **Required**: True
    - **Type**: list
    - **Default**: none
    - **Description**: List of JUnit XML report files to convert to JSON

  
  
  

  - **junit2json_do_merge**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
    - **Description**: Should we merge data of converted reports into 1 file or not.
When `false`, each report `XML` file is converted to a corresponding json file appended `.json` extension
Otherwise, resulting merged report is named as the directory, with `.report.json` extension.
in both cases, the result is stored under `junit2json_output_dir`.

  
  
  

  - **junit2json_output_dir**
    - **Required**: True
    - **Type**: str
    - **Default**: none
    - **Description**: Output directory for resulting report JSON file path(s)

  
  
  

  - **junit2json_input_merged_report**
    - **Required**: False
    - **Type**: str
    - **Default**: merged.junit.xml
    - **Description**: Relative file name for the Merged XML report (relevant only when `junit2json_do_merge` is `true`),
it is generated under `junit2json_output_dir`

  
  
  

  - **junit2json_output_merged_report**
    - **Required**: False
    - **Type**: str
    - **Default**: merged.junit.json
    - **Description**: Relative file name for the JSON report (relevant only when `junit2json_do_merge` is `true`),
it is generated under `junit2json_output_dir`

  
  
  

  - **global_json_reports_list**
    - **Required**: False
    - **Type**: list
    - **Default**: []
    - **Description**: This is the output variable updated by the role for the converted JSON reports file names.
If it is defined outside of the role, the role updates it.

  
  
  



</details>


### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [global_json_reports_list](defaults/main.yml#L6)   | list   | `[]` |    n/a  |  n/a |
| [junit2json_input_merged_report](defaults/main.yml#L9)   | str   | `merged.junit.xml` |    n/a  |  n/a |
| [junit2json_output_merged_report](defaults/main.yml#L10)   | str   | `merged.junit.json` |    n/a  |  n/a |
| [junit2json_do_merge](defaults/main.yml#L11)   | bool   | `True` |    n/a  |  n/a |





### Tasks


#### File: tasks/convert.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Read file content | ansible.builtin.set_fact | False |
| Update junit2json_result_data junit2json_do_merge=true | ansible.builtin.set_fact | False |
| Setup JSON report file name | ansible.builtin.set_fact | False |
| Set junit2json_output_report_path | ansible.builtin.set_fact | False |
| Update output variable global_json_reports_list | ansible.builtin.set_fact | False |
| Create folder junit2json_output_dir='{{ junit2json_output_dir }}' | ansible.builtin.file | False |
| Write files - data + hash file | ansible.builtin.copy | False |

#### File: tasks/validate-dependency.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Check if python dependency is installed - {{ item.package }} | ansible.builtin.command | False |
| Respond to the case if the dependency is not installed | ansible.builtin.assert | False |

#### File: tasks/merge.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Merge multiple JUnit XML files into single consolidated report | ansible.builtin.command | False |
| Write merge resulting file | ansible.builtin.copy | True |
| Override the list of JUnit XML files with merged JUnit XML file path | ansible.builtin.set_fact | False |

#### File: tasks/expand.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Print file_name value | ansible.builtin.debug | False |
| Collect file_name stat | ansible.builtin.stat | False |
| Verify file_name exists and is a regular file | ansible.builtin.assert | False |
| Update junit2json_reports_list with a JUnit XML report item | ansible.builtin.set_fact | True |

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Check dependencies | ansible.builtin.include_tasks | False |
| Validate role variables | ansible.builtin.assert | False |
| Print input reports variable | ansible.builtin.debug | False |
| Initialize reports variable | ansible.builtin.set_fact | False |
| Expand the input list to list of existing files | ansible.builtin.include_tasks | False |
| Merge JUnit XML reports into one file junit2json_do_merge=true | ansible.builtin.include_tasks | True |
| Convert XML to JSON | ansible.builtin.include_tasks | True |


## Task Flow Graphs



### Graph for convert.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Read_file_content0[read file content]:::task
  Read_file_content0-->|Task| Update_junit2json_result_data_junit2json_do_merge_true1[update junit2json result data junit2json do merge<br>true]:::task
  Update_junit2json_result_data_junit2json_do_merge_true1-->|Task| Setup_JSON_report_file_name2[setup json report file name]:::task
  Setup_JSON_report_file_name2-->|Task| Set_junit2json_output_report_path3[set junit2json output report path]:::task
  Set_junit2json_output_report_path3-->|Task| Update_output_variable_global_json_reports_list4[update output variable global json reports list]:::task
  Update_output_variable_global_json_reports_list4-->|Task| Create_folder_junit2json_output_dir__junit2json_output_dir_5[create folder junit2json output dir  junit2json<br>output dir ]:::task
  Create_folder_junit2json_output_dir__junit2json_output_dir_5-->|Task| Write_files___data___hash_file6[write files   data   hash file]:::task
  Write_files___data___hash_file6-->End
```


### Graph for validate-dependency.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Check_if_python_dependency_is_installed______item_package___0[check if python dependency is installed      item<br>package   ]:::task
  Check_if_python_dependency_is_installed______item_package___0-->|Task| Respond_to_the_case_if_the_dependency_is_not_installed1[respond to the case if the dependency is not<br>installed]:::task
  Respond_to_the_case_if_the_dependency_is_not_installed1-->End
```


### Graph for merge.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Merge_multiple_JUnit_XML_files_into_single_consolidated_report0[merge multiple junit xml files into single<br>consolidated report]:::task
  Merge_multiple_JUnit_XML_files_into_single_consolidated_report0-->|Task| Write_merge_resulting_file1[write merge resulting file<br>When: **junit2json merged xml stdout   length   10**]:::task
  Write_merge_resulting_file1-->|Task| Override_the_list_of_JUnit_XML_files_with_merged_JUnit_XML_file_path2[override the list of junit xml files with merged<br>junit xml file path]:::task
  Override_the_list_of_JUnit_XML_files_with_merged_JUnit_XML_file_path2-->End
```


### Graph for expand.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Print_file_name_value0[print file name value]:::task
  Print_file_name_value0-->|Task| Collect_file_name_stat1[collect file name stat]:::task
  Collect_file_name_stat1-->|Task| Verify_file_name_exists_and_is_a_regular_file2[verify file name exists and is a regular file]:::task
  Verify_file_name_exists_and_is_a_regular_file2-->|Task| Update_junit2json_reports_list_with_a_JUnit_XML_report_item3[update junit2json reports list with a junit xml<br>report item<br>When: **junit2json path item stat stat exists   default<br>false**]:::task
  Update_junit2json_reports_list_with_a_JUnit_XML_report_item3-->End
```


### Graph for main.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Include task| validate_dependency_yml0[check dependencies<br>include_task: validate dependency yml]:::includeTasks
  validate_dependency_yml0-->|Task| Validate_role_variables1[validate role variables]:::task
  Validate_role_variables1-->|Task| Print_input_reports_variable2[print input reports variable]:::task
  Print_input_reports_variable2-->|Task| Initialize_reports_variable3[initialize reports variable]:::task
  Initialize_reports_variable3-->|Include task| expand_yml4[expand the input list to list of existing files<br>include_task: expand yml]:::includeTasks
  expand_yml4-->|Include task| merge_yml5[merge junit xml reports into one file junit2json<br>do merge true<br>When: **junit2json do merge and junit2json reports list  <br>length   0**<br>include_task: merge yml]:::includeTasks
  merge_yml5-->|Include task| convert_yml6[convert xml to json<br>When: **junit2json reports list   length   0**<br>include_task: convert yml]:::includeTasks
  convert_yml6-->End
```


## Playbook

```yml
---

- name: "Test redhatci.ocp.junit2json role :: simple input"
  hosts: localhost
  vars:
    junit2json_output_merged_report: 'merged.junit.json'
  tasks:
    - name: Test role redhatci.ocp.junit2json without merge
      ansible.builtin.include_role:
        name: redhatci.ocp.junit2json
      vars:
        junit2json_input_reports_list:
          - "{{ role_path }}/../../tests/unit/data/test_junit2obj_simple_input.xml"
        junit2json_output_dir: "{{ role_path }}/tests"
        junit2json_do_merge: false
    - name: Load actual result to variable actual
      ansible.builtin.set_fact:
        actual: "{{ lookup('file', playbook_dir + '/test_junit2obj_simple_input.json') | from_json }}"
    - name: Load expected result to variable expected
      ansible.builtin.set_fact:
        expected: "{{ lookup('file', playbook_dir + '/../../../tests/unit/data/test_junit2obj_simple_result.json') }}"
    - name: Ensure both are identical
      ansible.builtin.assert:
        that:
          - actual == expected
    - name: Reset global variable
      ansible.builtin.set_fact:
        global_json_reports_list: []
    - name: Test role redhatci.ocp.junit2json with merge
      ansible.builtin.include_role:
        name: redhatci.ocp.junit2json
      vars:
        junit2json_input_reports_list:
          - "{{ role_path }}/../../tests/unit/data/test_junit2obj_simple_input.xml"
          - "{{ role_path }}/../../tests/unit/data/test_junit2obj_failure_input.xml"
        junit2json_output_dir: "{{ role_path }}/tests"
        junit2json_do_merge: true
    - name: Load actual result to variable actual
      ansible.builtin.set_fact:
        actual: "{{ lookup('file', global_json_reports_list[0]) | from_json }}"
    - name: Load expected result to variable expected
      ansible.builtin.set_fact:
        expected: "{{ lookup('file', playbook_dir + '/../../../tests/unit/data/' + junit2json_output_merged_report) }}"
    - name: Ensure both are identical
      ansible.builtin.assert:
        that:
          - actual == expected

```
## Playbook graph
```mermaid
flowchart TD
  localhost-->|Include role| redhatci_ocp_junit2json0(test role redhatci ocp junit2json without merge<br>include_role: redhatci ocp junit2json):::includeRole
  redhatci_ocp_junit2json0-->|Task| Load_actual_result_to_variable_actual1[load actual result to variable actual]:::task
  Load_actual_result_to_variable_actual1-->|Task| Load_expected_result_to_variable_expected2[load expected result to variable expected]:::task
  Load_expected_result_to_variable_expected2-->|Task| Ensure_both_are_identical3[ensure both are identical]:::task
  Ensure_both_are_identical3-->|Task| Reset_global_variable4[reset global variable]:::task
  Reset_global_variable4-->|Include role| redhatci_ocp_junit2json5(test role redhatci ocp junit2json with merge<br>include_role: redhatci ocp junit2json):::includeRole
  redhatci_ocp_junit2json5-->|Task| Load_actual_result_to_variable_actual6[load actual result to variable actual]:::task
  Load_actual_result_to_variable_actual6-->|Task| Load_expected_result_to_variable_expected7[load expected result to variable expected]:::task
  Load_expected_result_to_variable_expected7-->|Task| Ensure_both_are_identical8[ensure both are identical]:::task
```

## Author Information
Max Kovgan

#### License

Apache-2.0

#### Minimum Ansible Version

2.9

#### Platforms

No platforms specified.
<!-- DOCSIBLE END -->