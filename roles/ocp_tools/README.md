# ocp_tools role

Download and set up the command line tools used across the collection.

Requires `gather_facts` (uses `ansible_distribution_major_version` to select the RHEL-specific build).

## Usage

| Name         | Required | Default | Description
| ----         | -------- | ------- | -----------
| ot_tools     | true     | None    | List of tools to set up. See [supported tools](#supported-tools).
| ot_dest      | false    | ""      | Directory where binaries are placed. When empty, a temporary directory is created.
| ot_version   | false    | ""      | Version to download. Default uses `stable` (latest GA). See [version handling](#version-handling).
| ot_major     | false    | "4"     | Major stream to use when `ot_version` is non-numeric (e.g. `stable`). See [version handling](#version-handling).
| ot_base_url  | false    | ""      | Optional full override of the base mirror URL (up to the version segment). See [version handling](#version-handling).
| ot_retries   | false    | 3       | Number of retries for the download operations.
| ot_delay     | false    | 10      | Delay in seconds between download retries.

## Return values

| Name    | Description
| ------- | -----------
| ot_bin  | Dictionary mapping each requested tool to the absolute path of its binary.
| ot_dir  | Resolved working directory where the binaries were placed.

## Supported tools

This is the list of tools currently supported by the role:

- opm
- oc (includes `kubectl`)
- oc-mirror (GA/`stable`/`latest` streams only, no dev preview yet)

## Version handling

When no `ot_version` is provided the role downloads the stable version of the current GA release.

The major stream in the path comes from `ot_version` when it is numeric, falls back to `ot_major`.
Set `ot_major` to pull the `stable` (or any non-numeric) stream of a different major, e.g.
`ot_major: "5"` for OpenShift v5.

| ot_version   | URL resolution
| ----------   | --------------
| (empty)      | `.../openshift-v<ot_major>/clients/ocp/stable`
| `X.Y.Z`      | `.../openshift-v<X>/clients/ocp/X.Y.Z`
| `X.Y.0-rc.N` | `.../openshift-v<X>/clients/ocp/X.Y.0-rc.N`
| `X.Y.0-ec.N` | `.../openshift-v<X>/clients/ocp-dev-preview/X.Y.0-ec.N`


For non-version specific resolution use `ot_base_url` and `ot_version`, example:

```yaml
ot_base_url: "https://mirror.openshift.com/pub/openshift-v5/clients/ocp-dev-preview"
ot_version: "candidate-5.0"
```

## Example

```yaml
- name: Set up oc and opm for a given OCP version
  ansible.builtin.include_role:
    name: redhatci.ocp.ocp_tools
  vars:
    ot_tools:
      - oc
      - opm
    ot_dest: "/path/to/dir"
    ot_version: "4.22.16"

- name: Use oc
  ansible.builtin.command:
    cmd: "{{ ot_bin.oc }} version --client"

- name: Render a catalog with opm
  ansible.builtin.command:
    cmd: "{{ ot_bin.opm }} render quay.io/org/image:latest"
```
