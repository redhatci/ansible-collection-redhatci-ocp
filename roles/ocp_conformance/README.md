# ocp_conformance

Run the OpenShift **conformance / end-to-end (e2e)** test suites against an
OpenShift cluster using the `openshift-tests` binary shipped in the
[ose-tests](https://catalog.redhat.com/software/containers/openshift4/ose-tests-rhel9/)
image (the downstream build of
[openshift/origin](https://github.com/openshift/origin)).

The role supports:

- **Connected clusters:** `openshift-tests` runs as-is and pulls the e2e test
  images directly from their upstream sources.
- **Disconnected / air-gapped clusters:** when both `oc_registry` and
  `oc_mirror_org` are set, the e2e test images are mirrored into the local
  registry on the host (reusing the
  [redhatci.ocp.mirror_images](../mirror_images/README.md) role), and the tests are
  run with `--from-repository` so every image is pulled from the mirror.

It produces JUnit XML results and a run log, and (by default) compresses the
results into a tarball.

## Requirements

- `podman` (and `skopeo`, used by `mirror_images`) available on the host.
- Python `kubernetes` client (for the `kubernetes.core` modules).
- A reachable OpenShift cluster and its kubeconfig.
- For disconnected runs: a local registry, an auth file with credentials for both
  the source (`quay.io`) and the mirror registry, and host connectivity to the
  source images at mirror time. Ensure the registry has roughly **30 GB** of free
  disk space for the mirrored test images.

## Role Variables

| Name               | Default                                                | Description                                                                                            |
| ------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `oc_image`         | `registry.redhat.io/openshift4/ose-tests-rhel9:latest` | Container image (including tag) providing the `openshift-tests` binary.                                |
| `oc_container_uid` | `<random string>`                                      | Optional fixed suffix for the podman container name. A random string is used when unset.               |
| `oc_kubeconfig`    | `""`                                                   | **Required.** Host path to the kubeconfig for the target cluster.                                      |
| `oc_suite`         | `openshift/conformance`                                | Conformance suite to execute (e.g. `openshift/conformance/parallel`, `kubernetes/conformance`).        |
| `oc_provider`      | `""`                                                   | Value for `openshift-tests --provider`. Omitted when empty (autodetected).                             |
| `oc_log_dir`       | `/tmp`                                                 | Top-level host directory for the role's output (see "Generated files" below).                          |
| `oc_registry_auth` | `""`                                                   | Host path to a registry auth file. Required for disconnected mirroring and private tests images.       |
| `oc_ca_cert`       | `""`                                                   | Optional host path to a CA certificate; mounted into the container and `update-ca-trust` is run.       |
| `oc_registry`      | `""`                                                   | Local mirror registry host (e.g. `registry.local`). Set with `oc_mirror_org` to run disconnected.      |
| `oc_mirror_org`    | `""`                                                   | Destination organization/namespace in the mirror registry. Set with `oc_registry` to run disconnected. |
| `oc_compress`      | `true`                                                 | Compress the `logs/` directory into a tarball.                                                         |
| `oc_cleanup`       | `true`                                                 | Remove the uncompressed `logs/` directory after compression.                                           |

## Generated files (under `oc_log_dir`)

`openshift-tests` writes all of its artifacts (JUnit XML, event/timeline JSON,
HTML reports, resource archives, etc.) flat into a role-owned `logs/`
subdirectory. The role then surfaces the JUnit files at the top level:

- `logs/` — the full raw output of the run (removed after compression when
  `oc_cleanup`).
- `junit*.xml`, `e2e-monitor-tests*.xml` — the JUnit result files, copied to the
  top level for direct consumption.
- `conformance-run.log` — the combined stdout/stderr of the `openshift-tests`
  run, copied to the top level. Useful when a suite runs no tests and produces
  no other output.
- `conformance-logs.tar.gz` — the compressed `logs/` directory (when `oc_compress`).

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
            oc_registry: "registry.local:5000"
            oc_mirror_org: "conformance"
            oc_registry_auth: "/home/user/pull-secret.json"
            oc_ca_cert: "/home/user/ca.pem"
            oc_suite: "openshift/conformance"
```

## License

Apache-2.0
