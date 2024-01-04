# SOS Report

Generate SOS report from a list of OCP nodes

## Requirements

In disconnected (air gapped) environments the image to use *must* exist prior the use of this role

## Variables

| Variable             | Default                                                            | Required  | Description                                                                        |
| -------------------- | ------------------------------------------------------------------ | --------- | ---------------------------------------------------------------------------------- |
| sos_report_nodes     | \<undefined\>                                                      | Yes       | A list of OCP node names to generate their SOS report.                             |
| sos_report_dir       | /tmp                                                               | No        | Directory to place the sos reports.                                                |
| sos_report_image     | registry.redhat.io/rhel9/support-tools                             | No        | Fully Qualified Artifact Reference of the image to use containing the sos command. |
| sos_report_oc_path   | /usr/local/bin/oc                                                  | No        | Path to oc client.                                                                 |
| sos_report_options:  | -k crio.all=on -k crio.logs=on -k podman.all=on -k podman.logs=on  | No        | The sos report options.                                                            |

## Example Playbook

- SOS report in a single node

```YAML
- name: SOS Report in a worker node
  ansible.builtin.include_role:
    name: redhatci.ocp.sos_report
  vars:
    sos_report_nodes:
      - worker-0
```

- SOS report in multiple nodes

```YAML
- name: SOS Report in multiple worker nodes
  ansible.builtin.include_role:
    name: redhatci.ocp.sos_report
  vars:
    sos_report_nodes:
      - worker-0
      - worker-1
      - worker-2
```

- SOS report in a disconnected environment with a custom directory and custom oc path

```YAML
- name: SOS Report in multiple worker nodes
  ansible.builtin.include_role:
    name: redhatci.ocp.sos_report
  vars:
    sos_report_nodes:
      - master-0
      - worker-0
    sos_report_image: my-registry.example.local/tooling/custom-support-tools
    sos_report_dir: "{{ my_log_directory }}"
    sos_report_oc_path: "{{ my_oc_path }}"
```
