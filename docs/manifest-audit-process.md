# Generated Manifest Audit Process

This document describes the checklist and procedure for auditing oc-mirror v2
output manifests when a serialization defect or data quality issue is discovered.

---

## Background

The oc-mirror v2 tool produces several Kubernetes manifest types when mirroring
operator catalogs to a disconnected registry. Each manifest type has required
fields that must be populated for the manifest to be usable by OpenShift. A
serialization defect in the tool can produce manifests where normally-populated
fields are absent, empty, or set to empty collection values (e.g. `status: {}`).

Affected manifest types:

| Kind | File pattern | Critical fields |
|------|-------------|-----------------|
| `ImageDigestMirrorSet` (IDMS) | `idms-*.yaml` | `spec.imageDigestMirrors` (non-empty list) |
| `ImageTagMirrorSet` (ITMS) | `itms-*.yaml` | `spec.imageTagMirrors` (non-empty list) |
| `CatalogSource` | `cs-*.yaml` | `spec.sourceType`, `spec.image` |
| `ClusterCatalog` | `cc-*.yaml` | `spec.source` |
| `UpdateService` | `update-service-*.yaml` | `spec.graphDataImage`, `spec.releases` |

---

## Verification Steps

### Step 1 — Run the validation script

```bash
./hack/validate_manifests.sh <manifest-output-directory>
```

The script exits 0 if all manifests pass and prints `OK: all N manifest(s)
passed validation.` Review any `ERROR:` lines printed to stderr before
proceeding.

### Step 2 — Verify each manifest type

#### ImageDigestMirrorSet (IDMS)

```bash
# Check spec.imageDigestMirrors is a non-empty list
python3 -c "
import yaml, sys
doc = yaml.safe_load(open(sys.argv[1]))
mirrors = doc.get('spec', {}).get('imageDigestMirrors', [])
print(f'imageDigestMirrors entries: {len(mirrors)}')
assert len(mirrors) > 0, 'EMPTY — defect detected'
" idms-oc-mirror.yaml
```

Checklist:
- [ ] `apiVersion: config.openshift.io/v1`
- [ ] `kind: ImageDigestMirrorSet`
- [ ] `metadata.name` non-empty
- [ ] `status` field absent or non-empty (not `{}`)
- [ ] `spec.imageDigestMirrors` is a list with at least one entry
- [ ] Each entry has both `source` and `mirrors` fields

#### ImageTagMirrorSet (ITMS)

Checklist:
- [ ] `apiVersion: config.openshift.io/v1`
- [ ] `kind: ImageTagMirrorSet`
- [ ] `metadata.name` non-empty
- [ ] `status` field absent or non-empty (not `{}`)
- [ ] `spec.imageTagMirrors` is a list with at least one entry
- [ ] Each entry has both `source` and `mirrors` fields

#### CatalogSource

Checklist:
- [ ] `apiVersion: operators.coreos.com/v1alpha1`
- [ ] `kind: CatalogSource`
- [ ] `metadata.name` and `metadata.namespace` non-empty
- [ ] `spec.sourceType` non-empty (typically `grpc`)
- [ ] `spec.image` is a fully qualified image reference

#### ClusterCatalog

Checklist:
- [ ] `apiVersion: catalogd.operatorframework.io/v1`
- [ ] `kind: ClusterCatalog`
- [ ] `metadata.name` non-empty
- [ ] `spec.source` is defined and contains `type` and `image` sub-fields
- [ ] `spec.source.image.ref` is a fully qualified image reference

#### UpdateService

Checklist:
- [ ] `apiVersion: updateservice.operator.openshift.io/v1`
- [ ] `kind: UpdateService`
- [ ] `metadata.name` non-empty
- [ ] `spec.graphDataImage` non-empty
- [ ] `spec.releases` non-empty

---

## GitOps and ACM Policy Compliance Verification

When manifests are consumed by a GitOps pipeline or ACM policy framework,
incomplete manifests cause silent reconciliation failures. Before committing
manifests to the policy repository:

1. Run `./hack/validate_manifests.sh <output-dir>` — exit code must be 0.
2. Verify that each manifest that would be applied by ACM/ArgoCD matches the
   expected structure for its target cluster version (e.g. classic OLM clusters
   use `CatalogSource`; OLM v1 clusters use `ClusterCatalog`).
3. Apply the manifests to a staging cluster and confirm that the relevant
   operator controller reports no errors:
   ```bash
   oc get idms,itms,catalogsource,clustercatalog -A
   oc describe idms idms-oc-mirror
   ```
4. If any field is empty or missing, do **not** commit the manifests. Proceed to
   the resolution steps below.

---

## Resolution Steps

When a manifest fails validation:

1. **Identify the scope**: run `./hack/validate_manifests.sh` over all output
   directories produced by the mirroring run to determine which manifest types
   are affected.

2. **Re-run mirroring**: if the defect is transient (e.g. caused by a partial
   push or network interruption), rerun the mirroring role with a clean
   workspace directory.

3. **Check tool version**: confirm the version of oc-mirror in use and compare
   against the known good version documented in the release notes.

4. **Quarantine the output**: move the defective manifest directory to a
   quarantine location and record the tool version, workspace path, and error
   output for further analysis.

5. **Do not propagate**: ensure the defective manifests are not committed to any
   GitOps repository or ACM policy source until the issue is resolved and all
   validation checks pass.

6. **Verify after fix**: after applying a fix or upgrading the tool, re-run the
   full mirroring pipeline and confirm that `./hack/validate_manifests.sh`
   exits 0 before proceeding.

---

## Automated Validation in the Role

The `oci_mirror` Ansible role runs `tasks/validate-manifests.yml` automatically
after every mirroring run when `om_validate_manifests: true` (the default).
This provides early detection of defective manifests before they are used
downstream.

To disable automatic validation (not recommended for production):

```yaml
om_validate_manifests: false
```

---

*See also: `hack/validate_manifests.sh`, `roles/oci_mirror/tasks/validate-manifests.yml`.*
