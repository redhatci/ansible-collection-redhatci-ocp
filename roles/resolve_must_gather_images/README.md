# Resolve Must-Gather Images

Resolves must-gather image short names to full image references using
the `relatedImages` from installed operator ClusterServiceVersion (CSV)
resources.

This allows pipeline configurations to specify short image names
(e.g. `ptp-must-gather`) instead of hardcoding full image references
with version tags or digests. The role queries the cluster to find the
exact image reference matching the installed operator version.

## How It Works

1. Queries all installed CSVs on the cluster.
2. Collects all `relatedImages` entries from the CSVs.
3. For each entry in `rmgi_images`:
   - If it contains a `/`, it is treated as a full image reference and
     passed through unchanged.
   - Otherwise, it is matched (substring) against the `relatedImages`
     name field and replaced with the full image reference.
4. Sets the resolved list as `dci_must_gather_images`.

## Variables

| Variable    | Default              | Required | Description                                      |
| ----------- | -------------------- | -------- | ------------------------------------------------ |
| rmgi_images | `["ose-must-gather"]` | No       | List of must-gather image entries to resolve      |

## Output

| Variable                | Description                              |
| ----------------------- | ---------------------------------------- |
| dci_must_gather_images  | List of resolved full image references   |

## Examples

### Resolve PTP and standard must-gather images

```yaml
- name: Resolve must-gather images
  ansible.builtin.include_role:
    name: redhatci.ocp.resolve_must_gather_images
  vars:
    rmgi_images:
      - "ose-must-gather"
      - "ptp-must-gather"
```

This resolves to something like:

```yaml
dci_must_gather_images:
  - "registry.redhat.io/openshift4/ose-must-gather@sha256:abc123..."
  - "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:def456..."
```

### Mix short names with full references

```yaml
- name: Resolve must-gather images
  ansible.builtin.include_role:
    name: redhatci.ocp.resolve_must_gather_images
  vars:
    rmgi_images:
      - "ose-must-gather"
      - "ptp-must-gather"
      - "registry.redhat.io/openshift4/custom-must-gather:latest"
```

### Use in a DCI pipeline configuration

```yaml
# In your pipeline YAML
dci_must_gather_images:
  - "ose-must-gather"
  - "ptp-must-gather"
  - "sriov-network-must-gather"
```

Then in the DCI agent plays (doa/doaa), before the must-gather step:

```yaml
- name: Resolve must-gather images from operator CSVs
  ansible.builtin.include_role:
    name: redhatci.ocp.resolve_must_gather_images
  vars:
    rmgi_images: "{{ dci_must_gather_images }}"
```

## Filter Plugin

This role uses the `redhatci.ocp.resolve_must_gather` filter plugin,
which can also be used standalone:

```yaml
- name: Resolve images inline
  ansible.builtin.set_fact:
    resolved: >-
      {{ my_images | redhatci.ocp.resolve_must_gather(related_images_list) }}
```
