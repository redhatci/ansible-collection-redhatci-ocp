# kubevirt_redfish

A role to deploy the kubevirt-redfish Redfish BMC emulator for KubeVirt virtual machines on OpenShift.

## Description

This role deploys kubevirt-redfish, which provides a Redfish BMC interface for managing KubeVirt virtual machines. It creates all required Kubernetes resources:

- Namespace
- ServiceAccount, Role, and RoleBinding (RBAC)
- Configuration Secret
- Deployment with health probes
- Service
- OpenShift Route (optional)

The role also supports teardown by setting `kr_state: absent`.

## Requirements

- An OpenShift cluster with KubeVirt installed
- Ansible collection: [kubernetes.core](https://galaxy.ansible.com/kubernetes/core)
- The kubevirt-redfish container image must be accessible from the cluster

## Role Variables

### Core Settings

| Variable            | Default                                                                   | Required | Description
| --------            | -------                                                                   | -------- | -----------
| kr_delete_namespace | false                                                                     | No       | Delete the namespace where kubevirt-redfish was deployed, used when kr_state is absent.
| kr_image            | registry.redhat.io/container-native-virtualization/kubevirt-redfish-rhel9 | No       | Container image for the server
| kr_helper_image     | registry.access.redhat.com/ubi10/ubi-minimal:latest                       | No       | Helper image for datavolume operations
| kr_namespace        | kubevirt-redfish                                                          | No       | Target namespace
| kr_sa_name          | kubevirt-redfish-sa                                                       | No       | ServiceAccount name
| kr_scope            | namespaced                                                                | No       | Deployment scope (namespaced/cluster)
| kr_state            | present                                                                   | No       | Desired state (present/absent)
| kr_version          | v4.22                                                                     | No       | The tag of the image to use

### Configuration

The role supports two mutually exclusive ways to provide the kubevirt-redfish configuration:

1. **Config file** (`kr_config_file`) — provide a pre-built `config.yaml` file. All config-related variables (`kr_vm_configs`, `kr_server_*`, `kr_datavolume_*`, etc.) are ignored.
2. **Variables** (`kr_vm_configs` + defaults) — the role builds the config from individual variables.

| Variable       | Default | Required | Description
| --------       | ------- | -------- | -----------
| kr_config_file | ""      | No       | Path to a pre-built config.yaml file
| kr_vm_configs  | []      | No       | List of VM configurations (required when kr_config_file is not set)

VM configuration object structure (used when `kr_config_file` is not set):

```yaml
- name: string         # Required: VM name
  namespace: string    # Required: VM namespace
  bmc_password: string # Required: BMC password for Redfish auth
```

### Server Settings

| Variable                | Default  | Required | Description
| --------                | -------  | -------- | -----------
| kr_server_host          | 0.0.0.0  | No       | Server bind address
| kr_server_port          | 8443     | No       | Server port
| kr_server_tls_enabled   | false    | No       | Enable TLS on the server
| kr_system_id_convention | legacy   | No       | Default system ID convention

### Logging

| Variable                   | Default | Required | Description
| --------                   | ------- | -------- | -----------
| kr_log_level               | info    | No       | App log level (debug/info/warning/error)
| kr_redfish_log_level       | INFO    | No       | Redfish log level (DEBUG/INFO/WARNING/ERROR)
| kr_redfish_logging_enabled | true    | No       | Enable Redfish logging

### Deployment Settings

| Variable                   | Default | Required | Description
| --------                   | ------- | -------- | -----------
| kr_replicas                | 1       | No       | Number of replicas
| kr_image_pull_policy       | Always  | No       | Image pull policy
| kr_deployment_wait         | true    | No       | Wait for deployment readiness
| kr_deployment_wait_timeout | 300     | No       | Wait timeout in seconds

### Resource Limits

| Variable                     | Default | Required | Description
| --------                     | ------- | -------- | -----------
| kr_resources_requests_memory | 512Mi   | No       | Memory request
| kr_resources_requests_cpu    | 100m    | No       | CPU request
| kr_resources_limits_memory   | 2Gi     | No       | Memory limit
| kr_resources_limits_cpu      | 500m    | No       | CPU limit

### Datavolume Settings

| Variable                           | Default             | Required | Description
| --------                           | -------             | -------- | -----------
| kr_datavolume_storage_size         | 5Gi                 | No       | Storage size
| kr_datavolume_allow_insecure_tls   | true                | No       | Allow insecure TLS
| kr_datavolume_storage_class        | managed-nfs-storage | No       | Storage class
| kr_datavolume_vm_update_timeout    | 2m                  | No       | VM update timeout
| kr_datavolume_iso_download_timeout | 30m                 | No       | ISO download timeout

### Networking

| Variable                 | Default   | Required | Description
| --------                 | -------   | -------- | -----------
| kr_service_type          | ClusterIP | No       | Service type (ClusterIP/NodePort/LoadBalancer)
| kr_create_route          | true      | No       | Create an OpenShift Route
| kr_route_tls_termination | edge      | No       | TLS termination (edge/passthrough/reencrypt)
| kr_route_insecure_policy | Redirect  | No       | Insecure edge policy (Allow/Redirect/None)

## Usage Examples

### Basic Deployment

```yaml
- name: Deploy kubevirt-redfish
  ansible.builtin.include_role:
    name: redhatci.ocp.kubevirt_redfish
  vars:
    kr_vm_configs:
      - name: worker-0
        namespace: kubevirt-redfish
        bmc_password: "{{ vault_worker0_bmc_password }}"
      - name: worker-1
        namespace: kubevirt-redfish
        bmc_password: "{{ vault_worker1_bmc_password }}"
```

### Deploy with a Config File

```yaml
- name: Deploy kubevirt-redfish with pre-built config
  ansible.builtin.include_role:
    name: redhatci.ocp.kubevirt_redfish
  vars:
    kr_config_file: "/path/to/kubevirt-redfish-config.yaml"
```

### Custom Configuration

```yaml
- name: Deploy kubevirt-redfish with custom settings
  ansible.builtin.include_role:
    name: redhatci.ocp.kubevirt_redfish
  vars:
    kr_namespace: "my-redfish"
    kr_image: "my-registry.example.com/kubevirt-redfish:v1.0"
    kr_replicas: 2
    kr_datavolume_storage_class: "ceph-rbd"
    kr_resources_limits_memory: "4Gi"
    kr_create_route: false
    kr_vm_configs:
      - name: node-0
        namespace: my-redfish
        bmc_password: "{{ vault_node0_password }}"
```

### Cluster-Scoped Deployment

```yaml
- name: Deploy kubevirt-redfish monitoring all namespaces
  ansible.builtin.include_role:
    name: redhatci.ocp.kubevirt_redfish
  vars:
    kr_scope: cluster
    kr_namespace: kubevirt-redfish
    kr_vm_configs:
      - name: worker-0
        namespace: tenant-a
        bmc_password: "{{ vault_worker0_password }}"
      - name: worker-1
        namespace: tenant-b
        bmc_password: "{{ vault_worker1_password }}"
```

### Teardown

```yaml
- name: Remove kubevirt-redfish
  ansible.builtin.include_role:
    name: redhatci.ocp.kubevirt_redfish
  vars:
    kr_state: absent
    kr_scope: cluster
    kr_namespace: kubevirt-redfish
```

## Notes

- RBAC rules are preconfigured for kubevirt-redfish's requirements (KubeVirt VMs, CDI datavolumes, core resources)
- `kr_scope: namespaced` creates Role + RoleBinding scoped to `kr_namespace`
- `kr_scope: cluster` creates ClusterRole + ClusterRoleBinding for cross-namespace access
- The configuration Secret contains BMC passwords and is handled with `no_log`
- Teardown deletes all created resources individually (Route, Service, Deployment, Secret, RBAC, ServiceAccount, Namespace)
- The container runs with `runAsNonRoot` and drops all capabilities
