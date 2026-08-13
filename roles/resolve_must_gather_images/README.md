# redhatci.ocp.resolve_must_gather_images

Resolves a list of must-gather short names (e.g. `must-gather`,
`ose-must-gather`) to fully-qualified image references by inspecting the
`relatedImages` field of all `ClusterServiceVersion` resources installed on
the target cluster.

When a short name cannot be matched in the cluster's image list, the role
constructs a fallback reference using the configurable registry prefix.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rmgi_images` | list | **yes** | — | List of must-gather short names to resolve. |
| `rmgi_fallback_registry` | str | no | `registry.redhat.io/openshift4` | Registry/repository prefix used when a short name cannot be resolved from the cluster. |
| `rmgi_kubeconfig` | str | no | `""` | Path to a kubeconfig file. Leave empty to use the currently active context. |

## Outputs

| Variable | Description |
|----------|-------------|
| `rmgi_resolved_images` | List of resolved fully-qualified image references (one per entry in `rmgi_images`). |
| `dci_must_gather_images` | Alias for `rmgi_resolved_images`. Consumed by downstream roles such as `mirror_images`. |

## Usage example

```yaml
- name: Resolve must-gather images from installed operators
  ansible.builtin.include_role:
    name: redhatci.ocp.resolve_must_gather_images
  vars:
    rmgi_images:
      - must-gather
      - ose-must-gather
    rmgi_kubeconfig: "{{ kubeconfig_path }}"

- name: Mirror must-gather images to the disconnected registry
  ansible.builtin.include_role:
    name: redhatci.ocp.mirror_images
  vars:
    mi_images: "{{ dci_must_gather_images }}"
```

## License

Apache 2.0
