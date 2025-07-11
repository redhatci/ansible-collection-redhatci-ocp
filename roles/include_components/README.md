# Include DCI components

Create and attach DCI components to DCI jobs from git repositories, RPMs, commit URLs or just listed.

The `include_components` role creates and attaches DCI components to the DCI jobs by generating them from provided resources. Possible resource inputs include RPM packages, Git repositories, and GitHub commits.

Follow this post to know more about [components](https://blog.distributed-ci.io/automate-dci-components.html).

## Requirements

- Git
- [DCI ansible modules](https://github.com/redhat-cip/dci-ansible)

## Parameters

Variables used by this role:

| Setting        | Required | Type   | Description
| -------------- | -------- | ------ | -----------
| ic_gits        | True     | List   | Mandatory. List of directories from GIT repositories to include as components.
| ic_dev_gits    | True     | List   | Mandatory. List of complimentary directories from GIT repositories to include as components.
| ic_rpms        | False    | List   | Optional. List of RPM names to include as components.
| ic_commit_urls | False    | List   | Optional. List of GitHub URLs pointing directly to code commits. The URL format is `https://github.com/organisation/reponame/commit/commit_hash` and should contain the full commit hash. See examples.
| ic_listed      | False    | List   | Optional. List of components, each element must contain name and version keys. The type key is optional, if not provided, it defaults to the value of name.

## Examples

Create a Git component providing the source directory

```yaml
- name: Create a Git component providing code source dir
  ansible.builtin.include_role:
    name: redhatci.ocp.include_components
  vars:
    ic_gits:
      - "{{ code_source_dir }}"
    ic_dev_gits: []
```

Create a component providing the commit URLs

```yaml
- name: Create a component providing repo_url and commit_id
  ansible.builtin.include_role:
  name: redhatci.ocp.include_components
  vars:
    ic_commit_urls:
      - "https://github.com/my-organisation/my-reponame/commit/b6bcc3506c0d84baa0c020f6b776a181b931f57a"
      - "https://github.com/redhat-openshift-ecosystem/openshift-preflight/commit/b6bcc3506c0d84baa0c020f6b776asfasfasdfa"
    ic_gits: []
    ic_dev_gits: []
```

Create a components providing a list

```yaml
- name: Create listed components
  ansible.builtin.include_role:
    name: redhatci.ocp.include_components
  vars:
    ic_gits:
      - "{{ code_source_dir }}"
    ic_dev_gits: []
    ic_listed:
      - name: component_name_1
        version: 0.1
      - name: component_name_2
        version: 0.1
        type: mytype

```
