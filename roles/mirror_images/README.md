# Mirror Images

Mirrors images from one repository to another.

## Variables

| Variable         | Default    | Required | Description
| ---------------- | ---------- | -------- | -----------
| mi_images        | undefined  | Yes      | List of images to mirror
| mi_registry      | undefined  | Yes      | The registry target where to copy the images
| mi_authfile      | undefined  | No       | An authfile with permissions to pull/push images to/from registries
| mi_dst_authfile  | undefined  | No       | An authfile with permissions to push the target images
| mi_options       | undefined  | No       | skopeo options while copying the images
| mi_src_authfile  | undefined  | No       | An authfile with permissions to pull the source images
| mi_dst_org       | ""         | No       | The organization target where to copy the images
| mi_random_tag    | false      | No       | Set a random tag on the target registry

## Requirements

- [Skopeo](https://github.com/containers/skopeo/blob/main/install.md)

## Usage example

* Mirroring a single image

```yaml
- name: Mirror image
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_images
  vars:
    mi_images:
      -  quay.io/centos/centos:stream10-development
    mi_registry: registry.example.com
```

* Mirroring multiple images with most possible options

```yaml
- name: Mirror images
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_images
  vars:
    mi_images:
      -  quay.io/centos/centos:stream10-development
      -  quay.io/centos/centos:stream9
      -  quay.io/centos/centos:stream8
      -  quay.io/private/image
    mi_registry: my.registry.local:4443
    mi_dst_authfile: /path/to/pullsecret-to-push-to-my-registry-local
    mi_src_authfile: /path/to/pullsecret-to-pull-from-private-image
    mi_options: "--preserve-digests"
    mi_dst_org: "some/path"
```
The use of `mi_dst_org`: "some/path" will copy the new images into a new repository organization. For instance if the source image is quay.io/centos/centos:stream9, the destination will be my.registry.local:4443/some/path/centos:stream9
