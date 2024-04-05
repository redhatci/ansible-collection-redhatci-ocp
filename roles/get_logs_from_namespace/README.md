# Get Logs from Namespace

Extracts multiple logs from pods and events in a Namespace.

- Get the last 8h logs from all the containers of all pods in a Namespace
- Get all events in a Namespace
- Get the status of all the pods in a Namespace

## Variables

| Variable | Default   | Required | Description                                        |
| -------- | --------- | -------- | -------------------------------------------------- |
| glfn_dir | undefined | No       | Path to the dir where extracted logs will be saved |
| glfn_ns  | undefined | Yes      | Namespace to extract logs from                     |
| glfn_oc  | undefined | Yes      | Path to the oc client                              |

## Examples

Extract logs from a custom namespace and place them in a provided directory

```yaml
- name: Get logs for custom namespace
  ansible.builtin.include_role:
    name: redhatci.ocp.get_logs_from_namespace
  vars:
    glfn_dir: "/path/to/logs"
    glfn_ns: "custom-namespace"
    glfn_oc: "/path/to/oc"
```

Extract logs from multiple namespaces

```yaml
- name: Get logs for custom namespace
  ansible.builtin.include_role:
    name: redhatci.ocp.get_logs_from_namespace
  vars:
    glfn_oc: "/path/to/oc"
  loop:
    - ns1
    - ns2
    - nsN
  loop_control:
    loop_var: glfn_ns
```
