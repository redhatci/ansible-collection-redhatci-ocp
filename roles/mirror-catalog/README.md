# Mirror Catalog

Mirrors a catalog and its related images. Produces two files that can be used to set mirroring in an OCP cluster.

## Role Variables

Name            | Required | Default | Description
----------------|----------| --------|-------------
mc_oc_tool_path | Yes      |         | The path to the oc<sup>1</sup> binary, e.g. '/path/to/oc'
mc_catalog      | Yes      |         | The Fully Qualified Artifact Reference, e.g. 'example.com/namespace/web:v1.0'
mc_registry     | Yes      | ""      | The registry where the catalog will be mirrored, e.g. 'registry.example.com' or 'reg.example.com:4443'
mc_pullsecret   | No       |         | The credential file to pull and/or push the images, e.g. '/path/to/pullsecret.json'

<sup>1</sup> It's recommended to use a [stable version of oc](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/)

## Dependencies

The following applications must be already present in the system.

- [skopeo](https://github.com/containers/skopeo/blob/main/install.md).
- [oc](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html).

## Outputs

The role copies the ImageContentSourcePolicy file generated into a temporary file with `icsp_<image-name>.` prefix.

The `icsp` file can be used directly to apply the image content source policies into a running cluster. Or, it could also be used by extracting the `repositoryDigestMirrors` from it, and combining it with [the install-config.yml from an IPI installation](https://openshift-kni.github.io/baremetal-deploy/4.8/Deployment.html#_modify_the_install_config_yaml_file_to_use_the_disconnected_registry_optional)

The role also sets a variable with the path to the file: `mc_icsp_file.path`

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
