# ocp_conformance

Run the OpenShift **conformance / end-to-end (e2e)** test suites against an OpenShift cluster using the
`openshift-tests` binary shipped in the [ose-tests](https://catalog.redhat.com/software/containers/openshift4/ose-tests-rhel9/)
image (the downstream build of [openshift/origin](https://github.com/openshift/origin)).

The role supports:

- **Connected clusters:** `openshift-tests` runs as-is and pulls the e2e test images directly from their
  upstream sources.
- **Disconnected / air-gapped clusters:** when both `oc_registry` and `oc_mirror_org` are set, the e2e
  test images are mirrored to a local registry (reusing [redhatci.ocp.mirror_images](../mirror_images/README.md)
  role), and the tests are run so every image is pulled from the mirror.

It produces JUnit XML results and a run log, and (by default) compresses the results into a tarball.

## Requirements

- `podman` and `skopeo` available on the host.
- Python `kubernetes` client (for the `kubernetes.core` modules).
- A reachable OpenShift cluster and its kubeconfig.
- An authfile to pull the `oc_image` test image.
- For disconnected runs: a local registry, an auth file with credentials for both
  the source `oc_image` and the mirror registry, and host connectivity to the
  source images at mirror time. Ensure the registry has roughly **30 GB** of free
  disk space for the mirrored test images.

## Role Variables

| Name                | Default                                         | Description
| ----                | -------                                         | ------------
| `oc_kubeconfig`     |                                                 | **Required** Host path to the kubeconfig for the target cluster.
| `oc_registry_auth`  |                                                 | **Required** Host path to a registry auth file. Required for pulling the `oc_image`. In disconnected it must include creds to push to the `oc_registry`.
| `oc_ca_cert`        | `""`                                            | Optional host path to a CA certificate; mounted into the container and `update-ca-trust` is run.
| `oc_cleanup`        | `true`                                          | Remove the uncompressed `logs/` directory after compression.
| `oc_compress`       | `true`                                          | Compress the `logs/` directory into a tarball.
| `oc_container_uid`  | `<random string>`                               | Optional fixed suffix for the podman container name. A random string is used when unset.
| `oc_container_user` | `1001:0`                                        | Non-root numeric UID, optionally with GID, capabilities are dropped and privilege escalation is disabled.
| `oc_extra_env`      | `{}`                                            | Additional environment variables for the test container. `KUBECONFIG` remains managed by the role.
| `oc_extra_volumes`  | `[]`                                            | Additional Podman volume specifications for the test container, in `HOST_PATH:CONTAINER_PATH[:OPTIONS]` format.
| `oc_image`          | `registry.redhat.io/openshift4/ose-tests-rhel9` | Image providing `openshift-tests`, uses `oc_version` as its tag.
| `oc_log_dir`        | `/tmp`                                          | Top-level host directory for the role's output (see "Generated files" below).
| `oc_mirror_org`     | `""`                                            | Destination organization/namespace in the mirror registry. Set with `oc_registry` to run disconnected.
| `oc_provider`       | `""`                                            | Value for `openshift-tests --provider`. Omitted when empty (autodetected).
| `oc_registry`       | `""`                                            | Local mirror registry host (e.g. `registry.local`). Set with `oc_mirror_org` to run disconnected.
| `oc_suite`          | `openshift/conformance`                         | Conformance suite to execute (e.g. `openshift/conformance/parallel`, `kubernetes/conformance`).
| `oc_version`        | `latest`                                        | OCP version to test, e.g. `4.22`.

## Generated files (under `oc_log_dir`)

`openshift-tests` writes all of its artifacts (JUnit XML, event/timeline JSON, HTML reports, resource
archives, etc.) flat into a role-owned `logs/` subdirectory.

- `logs/`:  Raw output of the run (removed after compression when `oc_cleanup`).
- `junit*.xml`, `e2e-monitor-tests*.xml`: JUnit result files, copied to the
  top level `oc_log_dir`.
- `conformance-run.log`: the combined stdout/stderr of the `openshift-tests` run, copied to the top level.
  Useful when a suite runs no tests and produces no other output.
- `conformance-image.json`: Test image reference, `oc_image`, `oc_version` and its Digest.
- `conformance-logs.tar.gz`: Compressed `logs/` directory (when `oc_compress`).

## Example Playbook

### Connected

```yaml
- hosts: bastion
  tasks:
      - name: Run OpenShift conformance
        ansible.builtin.include_role:
            name: redhatci.ocp.ocp_conformance
        vars:
            oc_kubeconfig: "/home/user/clusterconfigs/kubeconfig"
            oc_registry_auth: "/home/user/pull-secret.json"
            oc_version: "4.22"
            oc_suite: "openshift/conformance"
            oc_log_dir: "/tmp/conformance"
```

### Disconnected / air-gapped

```yaml
- hosts: bastion
  tasks:
      - name: Run OpenShift conformance (disconnected)
        ansible.builtin.include_role:
            name: redhatci.ocp.ocp_conformance
        vars:
            oc_kubeconfig: "/home/user/clusterconfigs/kubeconfig"
            oc_version: "v4.22"
            oc_registry: "registry.local:5000"
            oc_mirror_org: "conformance"
            oc_registry_auth: "/home/user/pull-secret.json"
            oc_ca_cert: "/home/user/ca.pem"
            oc_suite: "openshift/conformance"
```

### Suite-specific configuration

Use `oc_extra_volumes` and `oc_extra_env` to provide files and environment variables required by a
particular suite without coupling this role to its consumer. For example, the [CSI suite](https://github.com/openshift/origin/tree/main/test/extended/storage/csi)
can receive a driver manifest:

```yaml
- hosts: bastion
  tasks:
      - name: Run OpenShift CSI tests
        ansible.builtin.include_role:
            name: redhatci.ocp.ocp_conformance
        vars:
            oc_kubeconfig: "/home/user/clusterconfigs/kubeconfig"
            oc_registry_auth: "/home/user/pull-secret.json"
            oc_version: "v4.22"
            oc_suite: "openshift/csi"
            oc_extra_volumes:
              - "/home/user/csi/manifest.yaml:/manifest.yaml:ro,z"
            oc_extra_env:
              TEST_CSI_DRIVER_FILES: "/manifest.yaml"
```

### Test image selection

`oc_version` is the primary image-selection input. The default `oc_image` uses the latest tag.
For testing specific OCP versions set the version of the cluster to test, including the prefix `v`,
e.g. `v4.20`.

`oc_image` can be overridden for specific cases such as a specific test build.
Doing so is an explicit compatibility decision: the caller is responsible for ensuring that image is
appropriate for the target cluster and the supplied `oc_version`.

Information about the test image used is stored under `conformance-image.json` for traceability.

## License

Apache-2.0
