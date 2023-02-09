# Mirror OCP release role

This role will mirror a given OpenShift release version to a given cache directory.  The directory is supposed to be served behind an HTTP server (e.g. Apache) so the cluster to be installed can reach it.

If enabled, the role requires an container registry to mirror the OCP container images.

## Variables

| Variable                    | Default       | Required    | Description                                                                                                                  |
| ----------------------------| ------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| mor_version                  | undefined     | Yes         | An OpenShift version number e.g. 4.10.45                                                                                     |
| mor_cache_dir                | /var/lib/dci-openshift-agent/releases | No          | Base directory that will hold the OCP version binaries and OS images                                 |
| mor_pull_url                 | undefined     | Yes          | The ocp release image URL for the release  |
| mor_force                    | false         | No          | If passed as true, the role will re-download all the OCP release resources                                                   |
| mor_mirror_disk_images       | true          | No          | Download all disk images depending on which install type                                                                     |
| mor_mirror_container_images  | true          | No          | Mirror all container images from upstream container registries to the provided registry                                      |
| mor_auths_file               | undefined     | Yes          | Path to the file containing all authentications needed for container registries e.g. $HOME/.docker/config.json |
| mor_write_custom_config      | true          | No          | Writes the OCP configuration files and sets the custom URL facts                                                             |
| mor_webserver_url            | undefined     | Yes         | URL of the web server where the installation artifact are stored|
| mor_registry_url             | undefined     | No*         | Required if `mor_mirror_container_images` is True. Registry where to mirror the upstream container images to                    |
| mor_registry_path            | ocp-\<version>/\<full_version\>| No        | Path in registry where the the release images will be stored. By default it is in the format of ocp-\<version>/\<full_version\>. For example: ocp-4.10/4.10.0-0.nightly-2023-02-16-193851 |
| mor_build                    | undefined     | Yes         | Build type (nightly, ga, dev, rc)  |
| mor_oc                       | undefined     | Yes         | Path to the oc binary (stable is recommended). |

## Requirements

- [Skopeo](https://github.com/containers/skopeo/blob/main/install.md)

## Usage example

See below for some examples of how to use the mirror-ocp-release role.

* Custom mirroring
```yaml
- name: Mirror release
  include_role:
    name: mirror-ocp-release
  vars:
    mor_version: "4.13.0-ec.1"
    mor_pull_url: "quay.io/openshift-release-dev/ocp-release@sha256:bb0d79219a876d87e994149c835033f8dcbf3433505a44a9e7e871b1b816b760"
    mor_cache_dir: "/opt/cache"
    mor_webserver_url: "https://<mywebserver>"
    mor_registry_url: "<my-registry>"
    mor_registry_path: "ocp4/openshift"
    mor_auths_file: "/var/<pull_secret>"
    mor_force: true
    mor_install_type: "ipi"
    mor_mirror_disk_images: true
    mor_mirror_container_images: true
    mor_write_custom_config: true
```

* Mirroring using default values
```yaml
- name: "Mirror release"
  include_role:
    name: mirror-ocp-release
  vars:
    mor_version: "4.12.0-0.nightly-2023-01-10-062211"
    mor_pull_url: "registry.ci.openshift.org/ocp/release@sha256:86b4185571e403a9bfcf82c4b363c4aaa41751976e60c1c10d1961e4b67ed9ab"
    mor_auths_file: "{{ dci_pullsecret_file }}"
    mor_webserver_url: "{{ webserver_url }}"
    mor_registry_url: "{{ dci_local_registry }}"
    mor_registry_path: "ocp-4.10/4.10.0-0.nightly-2023-02-16-193851"
```
