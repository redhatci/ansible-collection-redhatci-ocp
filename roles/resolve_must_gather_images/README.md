# Resolve Must-Gather Images

Resolves must-gather hints to full image references using installed
operator ClusterServiceVersion (CSV) resources.

This allows pipeline configurations to specify hints (e.g. `ptp`,
`acm`, `gitops`) instead of hardcoding full image references with
version tags or digests. The role queries the cluster to find the
exact image for the installed operator version.

## How It Works

1. Queries all installed CSVs on the cluster (`!olm.copiedFrom`).
2. Identifies CSVs that match each hint using the CSV name, displayName,
   annotations, and `relatedImages`.
3. For each matching CSV, takes the image in this order:
   1. `operators.openshift.io/must-gather-image` annotation
   2. Other CSV annotations whose key contains `must-gather`
      (e.g. Service Mesh `images.v1_28_8.must-gather`)
   3. `spec.relatedImages` entries whose name or image path contains
      `must-gather` or `mustgather` (e.g. OADP `oadp-mustgather-rhel9`)
4. Full image references (containing `/`) are ignored; pass those to
   must-gather separately.
5. Hints that cannot be resolved are **omitted** from the result. The
   role does not invent a registry path for missing operators.
6. Duplicate pullspecs are returned once (e.g. `mce` and
   `multicluster-engine`).
7. Sets the resolved list as `rmgi_resolved_images`.

## Variables

| Variable    | Default | Required | Description                                                                                         |
| ----------- | ------- | -------- | --------------------------------------------------------------------------------------------------- |
| rmgi_images | `[]`    | No       | List of hints that identify operators. Image names and other full references are ignored. Unresolved hints are dropped. |

## Output

| Variable             | Description                            |
| -------------------- | -------------------------------------- |
| rmgi_resolved_images | List of resolved full image references |

## Examples

### Resolve common operator must-gather images

`rmgi_images` is a list of hints that identify the operator, not
image names. Prefer the CSV or package name when a shorter hint is
ambiguous (for example `oadp-operator` instead of `oadp`). Some
operators advertise the operator image itself as must-gather (for
example Lifecycle Agent).

```yaml
- name: Resolve must-gather images
  ansible.builtin.include_role:
    name: redhatci.ocp.resolve_must_gather_images
  vars:
    rmgi_images:
      - acm
      - mce
      - multicluster-engine
      - ptp
      - gitops
      - lvms
      - oadp-operator
      - migration-toolkit-virtualization
      - istio
      - lifecycle-agent
      - kmm
      - cluster-logging
      - local-storage
      - openshift-compliance
```

This resolves to something like:

```yaml
rmgi_resolved_images:
  - registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:...
  - registry.redhat.io/multicluster-engine/must-gather-rhel9@sha256:...
  - registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:...
  - registry.redhat.io/openshift-gitops-1/must-gather-rhel9@sha256:...
  - registry.redhat.io/lvms4/lvms-must-gather-rhel9@sha256:...
  - registry.redhat.io/oadp/oadp-mustgather-rhel9@sha256:...
  - registry.redhat.io/migration-toolkit-virtualization/mtv-must-gather-rhel8@sha256:...
  - registry.redhat.io/openshift-service-mesh/istio-must-gather-rhel9@sha256:...
  - registry.redhat.io/openshift4/lifecycle-agent-rhel9-operator@sha256:...
  - registry.redhat.io/kmm/kernel-module-management-must-gather-rhel9@sha256:...
  - registry.redhat.io/openshift5/ose-local-storage-mustgather-rhel9@sha256:...
  - registry.redhat.io/compliance/openshift-compliance-must-gather-rhel8@sha256:...
```

`mce` and `multicluster-engine` resolve to the same pullspec and are
returned once. Hints for operators that are not installed (for example
`cluster-logging` above) are omitted.

## Filter Plugin

This role uses the `redhatci.ocp.resolve_must_gather` filter plugin,
which can also be used standalone:

```yaml
- name: Resolve images inline
  ansible.builtin.set_fact:
    resolved: >-
      {{ my_images | redhatci.ocp.resolve_must_gather(csv_lookup_list) }}
```
