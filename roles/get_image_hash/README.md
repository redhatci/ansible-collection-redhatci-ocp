# Get image hash role

Uses `skopeo` to produce a dictionary of image digests for images defined in `images_to_get_hash_for`.

## Requirements

- skopeo
- jq

## Role Variables

- `openshift_full_version`: used to set the tag for `ocp-release` which is one of the default images to fetch.
- `destination_hosts`: the hosts to put the `image_hashes`.

## Example Playbook

```yaml
- name: Play to populate image_hashes for relevant images
  hosts: localhost
  vars:
    destination_hosts:
      - registry_host
    openshift_full_version: 4.6.18
  roles:
    - get_image_hash
```
