# forgejo_setup

A role to deploy and configure Forgejo Git service

## Description

This role sets up a complete Forgejo Git service installation with:
- Pod to host the application and database containers
- PostgreSQL database backend (containerized)
- Forgejo application server (containerized)
- Persistent storage for data and database
- Health checks for both services

All containers run in rootless mode within a single pod

## Requirements

- [Podman](https://podman.io)
- Ansible collection: [containers.podman](https://galaxy.ansible.com/containers/podman)
- Enough disk space for Git repos and DB

## Variables

| Variable                | Default                            | Description
| ----------------------- | ---------------------------------- | -----------
| fs_state                | present                            | State of the deployment (present/absent)
| fs_app_container_name   | forgejo                            | Application container name
| fs_app_env_vars         | {}                                 | Additional environment variables for the application
| fs_app_image            | codeberg.org/forgejo/forgejo:13    | Forgejo container image
| fs_app_email            | `fs_app_user`@`fs_server_domain`   | Application admin email
| fs_app_name             | Forgejo: Beyond coding. We forge.  | Application name
| fs_app_password         | <auto generated>                   | Application password automatically generated if not set
| fs_app_user             | forgejo                            | Application admin user
| fs_base_dir             | {{ ansible_env.HOME }}/forgejo     | Base directory for all Forgejo data
| fs_data_dir             | {{ fs_base_dir }}/data             | Directory for Forgejo application data
| fs_db_container_name    | db                                 | DB container name
| fs_db_container_dir     | /var/lib/postgresql/18/docker      | Database data directory inside the container
| fs_db_dir               | {{ fs_base_dir }}/db               | Directory for DB data
| fs_db_name              | forgejo                            | DB name
| fs_db_password          | <auto generated>                   | DB password automatically generated if not set
| fs_db_user              | forgejo                            | DB user
| fs_pod_http_port        | 3000                               | Host port for Forgejo HTTP interface
| fs_pod_name             | forgejo                            | Podman pod name
| fs_pod_ssh_port         | 2222                               | Host port for Forgejo SSH interface
| fs_postgres_image       | mirror.gcr.io/library/postgres:18  | DB container image
| fs_user                 | {{ ansible_user_id }}              | User to run containers as (rootless mode)
| fs_user_gid             | {{ ansible_user_gid }}             | GID of the user running containers
| fs_user_uid             | {{ ansible_user_uid }}             | UID of the user running containers
| fs_wait_delay           | 10                                 | Delay in seconds between retries
| fs_wait_retries         | 30                                 | Number of retries when waiting for services
| fs_server_domain        | localhost                          | Domain name for the Forgejo server
        
> [!IMPORTANT]
> The `fs_db_container_dir` path depends on the version of postgres

## Dependencies

- containers.podman collection

## Usage Examples

### Basic Deployment

```yaml
- name: Deploy Forgejo with PostgreSQL
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_setup
```

### Custom Configuration

```yaml
- name: Deploy Forgejo with custom settings
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_setup
  vars:
    fs_pod_http_port: 8080
    fs_pod_ssh_port: 2222
    fs_postgres_password: "secure_password_here"
    fs_base_dir: /opt/forgejo
    fs_forgego_server: git.example.com
    fs_app_env_vars:
      FORGEJO__server__DOMAIN: "{{ fs_forgego_server }}"
      FORGEJO__server__ROOT_URL: "https://{{ fs_forgego_server }}"
      FORGEJO__server__SSH_DOMAIN: "{{ fs_forgego_server }}"
```

### Remove Forgejo Deployment

```yaml
- name: Remove Forgejo installation
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_setup
  vars:
    fs_state: absent
```

## Post-Installation

Access Forgejo at `http://localhost:3000` (or your custom port) with the credentials provided or generated during deployment.

## Troubleshooting

### Check pod and container status

```bash
podman pod ps
podman ps -a --pod
```

### View container logs

```bash
podman logs forgejo
podman logs db
```

### Restart pod

```bash
podman pod restart forgejo
```

### Access database files

The database directory is owned by the mapped container UID due to rootless Podman's user namespace mapping.
To access database files as the container user for backup or management:

```bash
podman unshare <cmd> /path/to/db
```

This allows you to interact with files using the same UID mapping that the container uses.

## License

Apache-2.0
