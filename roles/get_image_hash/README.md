# Get image hash role

Uses `skopeo` to produce a dictionary of image digests for images defined in `images_to_get_hash_for`.

## Requirements

- skopeo
- jq


## Role Variables

| Variable                      | Required  | Type             | Default   | Description
| ----------------------------- | --------- | ---------------- | --------- | -----------
| os_images                     | Yes       | Array of Objects  | Undefined | Used by assisted installer to populate values the version which can be used. |
| release_images                | Yes       | Array of Objects  | Undefined | Used by agent based installer to find the image to extract the installer from. It is also used by assisted installer to populate the version which can be used. |
| openshift_full_version        | Yes       | string            | Undefined | used to select the correct release_images entry to fetch. |
| destination_hosts             | Yes       | Array  | ['bastion', 'localhost', 'registry_host', 'assisted_installer'] | the hosts to put the resulting `image_hashes`.



## Example Playbook

```yaml
- name: Play to populate image_hashes for relevant images
  hosts: localhost
  vars:
    os_images:
      - openshift_version: '4.14'
        cpu_architecture: x86_64
        url: https://mirror.openshift.com/pub/openshift-v4/x86_64/dependencies/rhcos/4.14/4.14.0/rhcos-4.14.0-x86_64-live.x86_64.iso
        rootfs_url: https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.14/4.14.0/rhcos-4.14.0-x86_64-live-rootfs.x86_64.img
        version: 414.92.202310170514-0
    release_images:
      - openshift_version: '4.14'
        cpu_architecture: x86_64
        url: quay.io/openshift-release-dev/ocp-release:4.14.2-x86_64
        version: 4.14.2
    destination_hosts:
      - assisted_installer
    openshift_full_version: 4.14.2
  roles:
    - get_image_hash
```
