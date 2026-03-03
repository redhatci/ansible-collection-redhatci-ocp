# Mirror OCP release role

This role will mirror a given OpenShift release version to a given cache directory.
In disconnected environments, the directory is expected to be served behind an HTTP server (e.g. Apache) so the cluster to be installed can reach it.

If enabled, the role requires a container registry to mirror the OCP container images.

## Variables

| Variable                     | Default                                                            | Required | Description
| ---------------------------- | ------------------------------------------------------------------ | -------- | -----------
| mor_auths_file               | undefined                                                          | No*      | Path to the authentication file used for container registries e.g. `$HOME/.docker/config.json`. Required when `mor_mirror_container_images` is True. Also required to download release artifacts.
| mor_cache_dir                | /var/lib/dci-openshift-agent/releases                              | No       | Base directory that will hold the OCP version binaries and OS images.
| mor_force                    | false                                                              | No       | If passed as true, the role will re-download all the OCP release resources.
| mor_install_type             | "ipi"                                                              | No       | Installation type(s) to include. Can be a **string** or a **list of strings**. Supported values: `ipi`, `sno`, `upi`, `assisted`, `vsphere`, `acm`, `abi`, `aws`, `azure`.
| mor_installer                | \<See Description\>                                                | No       | Depending on the OCP 4.16+:`openshift-install`, 4.16-:`openshift-baremetal-install`.
| mor_is_type                  | \<See Description\>                                                | No       | Image Source file type. Default: `icsp` for 4.13 and below, `idms` for 4.14 and above.
| mor_list_install_type        | ['ipi','sno','upi','assisted','vsphere','acm','abi','aws','azure'] | No       | List of supported install types used internally by the role.
| mor_mirror_container_images  | true                                                               | No       | Mirror all container images from upstream container registries to the provided registry.
| mor_mirror_disk_images       | true                                                               | No       | Download all disk images depending on which install type.
| mor_oc                       | undefined                                                          | Yes      | Path to the oc binary (stable is recommended).
| mor_pull_url                 | undefined                                                          | Yes      | The ocp release image URL for the release.
| mor_registry_path            | ocp-\<version\>/\<full_version\>                                   | No       | Repository to mirror release images. For example: ocp-4.20/4.20.0-0.nightly-2026-01-02-123456.
| mor_registry_url             | undefined                                                          | No*      | Required when `mor_mirror_container_images` is True. Registry to mirror the release images to.
| mor_version                  | undefined                                                          | Yes      | An OpenShift version number e.g. 4.20.15.
| mor_webserver_url            | undefined                                                          | No*      | URL of the web server where the installation artifacts are stored. Required when `mor_write_custom_config` is True (default).
| mor_write_custom_config      | true                                                               | No       | Writes the OCP configuration files and sets the custom URL facts. Requires `mor_webserver_url` to be set.
| mor_allow_insecure_registry  | true                                                               | No       | Allow interacting with registries that are using an unknown CA certificate.
| mor_extra_flags              | ""                                                                 | No       | Extra flags to pass to the `oc adm release mirror` command when mirroring release images.


## Requirements

- [Skopeo](https://github.com/containers/skopeo/blob/main/install.md)

## Usage example

See below for some examples of how to use the mirror_ocp_release role.

* Custom mirroring
```yaml
- name: Mirror release
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_ocp_release
  vars:
    mor_version: "4.15.0-ec.1"
    mor_pull_url: "quay.io/openshift-release-dev/ocp-release@sha256:bb0d79219a876d87e994149c835033f8dcbf3433505a44a9e7e871b1b816b760"
    mor_cache_dir: "/opt/cache"
    mor_webserver_url: "https://<mywebserver>"
    mor_registry_url: "<my-registry>"
    mor_registry_path: "ocp4/openshift"
    mor_auths_file: "/var/<pull_secret>"
    mor_force: true
    mor_install_type: "ipi"
    mor_is_type: "idms"
    mor_mirror_disk_images: true
    mor_mirror_container_images: true
    mor_write_custom_config: true
```

* Mirroring using default values
```yaml
- name: "Mirror release"
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_ocp_release
  vars:
    mor_version: "4.14.0-0.nightly-2024-01-10-123456"
    mor_pull_url: "registry.ci.openshift.org/ocp/release@sha256:86b4185571e403a9bfcf82c4b363c4aaa41751976e60c1c10d1961e4b67ed9ab"
    mor_auths_file: "{{ my_pullsecret_file }}"
    mor_is_type: "icsp"
    mor_webserver_url: "{{ webserver_url }}"
    mor_registry_url: "{{ my_local_registry }}"
    mor_registry_path: "ocp-4.14/4.14.0-0.nightly-2024-01-10-123456"
```
