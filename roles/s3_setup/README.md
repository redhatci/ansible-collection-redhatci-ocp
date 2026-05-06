# s3_setup

A role to deploy S3-compatible object storage as a standalone Podman container or in a Kubernetes/OpenShift cluster.

Currently uses [MinIO](https://min.io/) as the S3 server implementation, [built by chainguard](https://images.chainguard.dev/directory/image/minio/overview). The server can be changed via the `ss_image` variable to use any S3-compatible server that follows the same CLI conventions (e.g. [RustFS](https://rustfs.com/)).

## Description

This role sets up an S3-compatible server with:
- S3 API endpoint
- Web management console
- Automatic bucket creation
- Persistent storage
- Health checks

Two deployment modes are available:
- **standalone** — rootless Podman container with optional systemd integration
- **k8s** — Kubernetes/OpenShift deployment with PVC, Service, and namespace isolation

## Requirements

### Standalone mode
- [Podman](https://podman.io)
- Ansible collection: [containers.podman](https://galaxy.ansible.com/containers/podman)

### k8s mode
- Access to a Kubernetes/OpenShift cluster
- Ansible collection: [kubernetes.core](https://galaxy.ansible.com/kubernetes/core)
- A storage class with ReadWriteMany (RWX) support (typically NFS-based)

## Variables

### Common variables

| Variable         | Default                    | Description
| ---------------- | -------------------------- | -----------
| ss_mode          | standalone                 | Deployment mode: 'standalone' or 'k8s'
| ss_state         | present                    | State of the deployment (present/absent)
| ss_image         | cgr.dev/chainguard/minio   | S3 server/client container image
| ss_username      | \<auto generated\>         | Root user (access key), auto-generated if not set
| ss_password      | \<auto generated\>         | Root password (secret key), auto-generated if not set
| ss_buckets       | []                         | List of bucket names to create
| ss_wait_retries  | 30                         | Number of retries when waiting for readiness
| ss_wait_delay    | 5                          | Delay in seconds between retries

### Standalone-specific variables

| Variable           | Default                  | Description
| ------------------ | ------------------------ | -----------
| ss_user            | {{ ansible_user_id }}    | User to run containers as (rootless mode)
| ss_user_home       | {{ ansible_user_dir }}   | Home directory of the user
| ss_user_uid        | {{ ansible_user_uid }}   | UID of the user running containers
| ss_user_gid        | {{ ansible_user_gid }}   | GID of the user running containers
| ss_base_dir        | $HOME/minio-server       | Base directory for data
| ss_data_dir        | {{ ss_base_dir }}/data   | Directory for data storage
| ss_container_name  | minio                    | Container name
| ss_server_domain   | localhost                | Domain name or IP address
| ss_api_port        | 9000                     | Host port for the S3 API
| ss_console_port    | 9001                     | Host port for the web console
| ss_use_systemd     | false                    | Whether to create systemd user units

### k8s-specific variables

| Variable          | Default      | Description
| ----------------- | ------------ | -----------
| ss_namespace      | minio        | Kubernetes namespace for the deployment
| ss_storage_class  | —            | **Required.** Storage class with RWX support
| ss_claim_size     | 10Gi         | PVC storage size request
| ss_service_type   | NodePort     | Kubernetes service type (NodePort, LoadBalancer, ClusterIP)

## Dependencies

### Standalone mode
- containers.podman collection

### k8s mode
- kubernetes.core collection

## Usage Examples

### Standalone: Basic Deployment

```yaml
- name: Deploy S3 server
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
```

### Standalone: Deployment with Custom Credentials

```yaml
- name: Deploy S3 server with custom credentials
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_username: minio-admin
    ss_password: my-secret-password
```

### Standalone: Deployment with Buckets and Systemd

```yaml
- name: Deploy S3 server with buckets
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_username: minio-admin
    ss_password: my-secret-password
    ss_buckets:
      - test-bucket
      - artifacts
    ss_use_systemd: true
```

### k8s: Deploy in OpenShift

```yaml
- name: Deploy S3 server in OpenShift
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_mode: k8s
    ss_storage_class: nfs-storage
    ss_buckets:
      - my-bucket
```

### k8s: Deploy with Custom Settings

```yaml
- name: Deploy S3 server in k8s with custom settings
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_mode: k8s
    ss_storage_class: nfs-storage
    ss_namespace: s3-prod
    ss_claim_size: 50Gi
    ss_service_type: LoadBalancer
    ss_username: minio-admin
    ss_password: my-secret-password
    ss_buckets:
      - artifacts
      - backups
```

### Remove Standalone Deployment

```yaml
- name: Remove S3 server installation
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_state: absent
    ss_use_systemd: true
```

### Remove k8s Deployment

```yaml
- name: Remove S3 server from cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.s3_setup
  vars:
    ss_mode: k8s
    ss_state: absent
```

## Troubleshooting

### Standalone

#### Check container status

```bash
podman ps -a | grep minio
```

#### View container logs

```bash
podman logs minio
```

#### Check health

```bash
curl http://localhost:9000/minio/health/live
```

#### Access the web console

Open `http://localhost:9001` in a browser and log in with the root credentials.

#### List buckets

```bash
podman exec minio mc alias set myminio http://localhost:9000 ACCESS_KEY SECRET_KEY
podman exec minio mc ls myminio/
```

### k8s

#### Check pod status

```bash
kubectl get pods -n minio
```

#### View pod logs

```bash
kubectl logs -n minio deployment/s3-server
```

#### Check service

```bash
kubectl get svc -n minio
```

## License

Apache-2.0
