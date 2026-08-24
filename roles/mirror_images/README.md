# Mirror Images

Mirrors images from one repository to another and generates an Image Source
manifest in a temporary file: `ImageContentSourcePolicy` (`icsp`), or both
`ImageDigestMirrorSet` and `ImageTagMirrorSet` (`idms`, for OCP 4.14+).

Mirroring always copies the listed images regardless of `mi_is_type`. The
generated Image Source is optional for callers that only need the mirror.

**ICSP and tags:** `icsp` emits `repositoryDigestMirrors` only. That remaps
digest pulls (`repo@sha256:...`), not `registry/repo:tag` pulls. If you apply
the ICSP and workloads still pull by tag, those pulls will not use the mirror.
Use digest-pinned `mi_images`, or set `mi_is_type=idms` (IDMS + ITMS) when tag
remapping is required.

## Variables

| Variable         | Default            | Required | Description
| ---------------- | ------------------ | -------- | -----------
| mi_images        | undefined          | Yes      | List of images to mirror (tags or digests)
| mi_registry      | undefined          | Yes      | The registry target where to copy the images
| mi_authfile      | undefined          | No       | An authfile with permissions to pull/push images to/from registries
| mi_dst_authfile  | undefined          | No       | An authfile with permissions to push the target images
| mi_options       | undefined          | No       | skopeo options while copying the images
| mi_src_authfile  | undefined          | No       | An authfile with permissions to pull the source images
| mi_dst_org       | ""                 | No       | The organization target where to copy the images
| mi_random_tag    | false              | No       | Copy to a random destination tag to avoid overwriting existing mirror content
| mi_is_type       | `idms`             | No       | Image Source file type: `icsp` (ImageContentSourcePolicy) or `idms` (ImageDigestMirrorSet + ImageTagMirrorSet). See note above about ICSP and tags.
| mi_is_name       | auto-generated     | No       | Metadata name for the Image Source resource. Default: `mirrored-images-<8-char-random>` each role run. Set explicitly to pin the name across runs.
| mi_verify_digest | false              | No       | When `true`, verify that the source and destination image digests match after a failed copy. When `false` (default), only verify that the destination image exists. Set to `false` when mirroring may occur in a separate step or access to the source registry is limited.

## Requirements

- [Skopeo](https://github.com/containers/skopeo/blob/main/install.md)

## Outputs

The role always generates an Image Source manifest and copies it into a temporary file with an `imagesource_mirror_images.` prefix. When `mi_is_type` is `idms`, the file contains an IDMS and, unless `mi_random_tag` is true, an ITMS.

- `mi_is_file.path`: Path to the generated Image Source file.
- `mi_image_mirrors`: List of mappings used to build the manifest:
  - `source`: source repository
  - `mirror`: mirror repository
  - `target`: full destination reference that was copied (includes tag)
  - `tag_preserved`: `false` when `mi_random_tag` rewrote the destination tag

The Image Source file can be applied directly to a running cluster.

## Usage example

* Mirroring a single image

```yaml
- name: Mirror image
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_images
  vars:
    mi_is_type: "idms"
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
    mi_is_type: "idms"
```

The use of `mi_dst_org`: "some/path" will copy the new images into a new repository organization. For instance if the source image is quay.io/centos/centos:stream9, the destination will be my.registry.local:4443/some/path/centos:stream9

* Apply the generated Image Source manifest

```yaml
- name: Mirror images
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_images
  vars:
    mi_images:
      - quay.io/example/image@sha256:abc123
    mi_registry: my.registry.local:4443
    mi_is_type: "idms"

- name: Apply Image Source file
  kubernetes.core.k8s:
    definition: "{{ lookup('file', mi_is_file.path) | from_yaml_all | list }}"
```
