# Mirror Catalog

Mirrors a catalog and its related images. Produces a file that can be used to set mirroring in an OCP cluster.

## Role Variables

Name            | Required | Default | Description
----------------|----------| --------|-------------
mc_oc_tool_path | Yes      |         | The path to the oc<sup>1</sup> binary, e.g. '/path/to/oc'
mc_catalog      | Yes      |         | The Fully Qualified Artifact Reference, e.g. 'example.com/namespace/web:v1.0'
mc_registry     | Yes      | ""      | The registry where the catalog will be mirrored, e.g. 'registry.example.com' or 'reg.example.com:4443'
mc_pullsecret   | No       |         | The credential file to pull and/or push the images, e.g. '/path/to/pullsecret.json'
mc_is_type      | No       | icsp    | The type of image source to use, choose between icsp (imageContentsourcePolicy) (default) or idms (imageDigestMirrorSet).

<sup>1</sup> It's recommended to use a [stable version of oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/)

## Dependencies

The following applications must be already present in the system.

- [skopeo](https://github.com/containers/skopeo/blob/main/install.md).
- [oc](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html).

## Outputs

The role copies a generated Image Sources manifest file into a temporary file with `imagesource_<image-name>.` prefix.

If a `KUBECONFIG` environment variable is set, the role will look into the cluster to determine the type of Image Source file to generate, for OCP 4.14 and above the Image Source file will contain `ImageDigestManifestSet` when such resource is in use, otherwise will use `ImageContentSourcePolicies`. OCP 4.13 and earlier will always contain `ImageContentSourcePolicies`.

The Image Source file can be used directly to apply the image source into a running cluster.

The role also sets a couple of variables

- `mc_is_file.path`: The path to the Image Source file produced.
- `mc_catalog_digest`: The catalog image using its digest.

## Example Playbook

As a role:

```yaml
- hosts: localhost
  roles:
     - role: mirror-catalog
       vars:
         mc_oc_tool_path: /path/to/oc
         mc_catalog: my.example.com/my-org/my-image:latest
         mc_registry: my-registry.example.com
         mc_is_type: "idms"
```

As a task:

```yaml
- name: Mirror catalog
  include_role:
    name: mirror-catalog
  vars:
    mc_oc_tool_path: "{{ path_to_oc }}"
    mc_catalog: my.example.com/my-org/my-image:latest
    mc_registry: "my-registry.example.com:4443"
    mc_pullsecret: /path/to/auth.json
```

## License

Apache License, Version 2.0
