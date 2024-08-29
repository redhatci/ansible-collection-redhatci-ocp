<!-- DOCSIBLE START -->
# efi_boot_mgr

Remove the non-active UEFI boot entries from OCP nodes.


## Requirements

Role Requirements go here

## Inputs

| Var  | Type  | Required | Default  | Description
| ---- | ----- | -------- | -------- | -----------
| ebm_nodes | list | True | \<undefined\> | A list of OCP node names to manage their Boot order.
| ebm_oc_path | str | False | /usr/local/bin/oc | Path to oc client.

## Variables 
| Var          | Type         | Value       | Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [ebm_oc_path](defaults/main.yml#L6)   | str   | `/usr/local/bin/oc`  |  false  |  Path to oc binary | 
<details>
<summary>🖇️ Full descriptions for vars in defaults/main.yml</summary>
<br>
<b>ebm_oc_path:</b> Allow to override the path of oc binary<br>
<br>
<br>
</details>
   

## Task Flow Graphs

### Graph for main.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef include stroke:#2ecc71,stroke-width:2px;
classDef import stroke:#f39c12,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;
classDef importPlaybook stroke:#9b59b6,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;

  Start-->|Task| Validation_for_UEFI_Boot_Manager0[validation for uefi boot manager]:::task
  Validation_for_UEFI_Boot_Manager0-->|Task| Delete_UEFI_boot_entries_in_nodes1[delete uefi boot entries in nodes]:::task
  Delete_UEFI_boot_entries_in_nodes1-->|Task| Check_boot_cleanup_status2[check boot cleanup status]:::task
  Check_boot_cleanup_status2-->End
```
## License

Apache-2.0


<!-- DOCSIBLE END -->