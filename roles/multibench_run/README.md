# Multi-bench role
This role is a standard procedure to launch a [Multi-bench](https://github.com/perftool-incubator/crucible) test.
It uses a pre-existing VM/host where all the crucible binaries are ready.

## Requirements
A PerformanceProfile must be correctly setup on your OCP before launching this playbook.
The multibench_host should have been prepared before running this role.
***Playbook for the setup in WIP***

| Variable              | Default                                                       | Type      | Required | Description                                                                                                  |
|-----------------------|---------------------------------------------------------------|-----------|----------|--------------------------------------------------------------------------------------------------------------|
| multibench_host       | null                                                          | string    | true     | Address of the multi-bench host accessible with SSH                                                          |
| multibench_output_dir | None                                                          | directory | false    | Directory where the results of the bench are copied                                                          |
| multibench_sample     | 3                                                             | Integer   | false    | Nb of time the benchmark will be run                                                                         |
| ocp_host              | Host with a working oc connection                             | string    | true     | Address of the host which has a valid kubeconfig, accessible with SSH                                        |
| multibench_script     | run.sh	                                                       | string    | false    | Name of the script to be executed for launching the crucible cmd. Located in the {{ multibench_script_dir }} |
| multibench_script_dir | /root/crucible-examples/all-in-one/openshift/example-A/daily	 | string    | false    | path of the multibench script on the multi-bench host                                                        |
| multibench_tags       | automation:ansible                                            | key:value | false    | tag to be added to the multi-bench Run in the Opensearch DB                                                  |

## Presentation of the workload
By default, the workload launched by default is the example-A of Multi-bench, composed of 2 uperf scenarios and 1 iperf.
![Multi-bench_example-A](images/example-A.png)

If you want to customize the scenarios, you can edit the `run.sh` file which defines the previous layout of test.
You can edit the resources requested by the pods (clients or servers), in order to have a Guaranteed QoS.
You can change the variable `multibench_script` to keep several scenarios ready and easily switch from one to another.

## Example - how to use the role
In this example, the two mandatory variable for the role are defined in the Ansible inventory:

```yaml
- name: "Include role multi-bench"
  include_role:
    name: redhatci.ocp.multibench_run
  vars:
    multibench_host: "{{ groups['multibench'] | first }}"
    ocp_host: "{{ groups['provisioner'] | first }}"

```