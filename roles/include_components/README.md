# redhat.ocp.include_components role - create and attach DCI components to the DCI jobs

- [Synopsis](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/include_components/README.md#synopsis)
- [Parameters](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/include_components/README.md#parameters)
- [Examples](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/include_components/README.md#examples)

# Synopsis

The `include_components` role creates and attaches DCI components to the DCI jobs by generating them from provided resources. Possible resource inputs include RPM packages, Git repositories, and Github commits.

Follow this post to know more about [components](https://blog.distributed-ci.io/automate-dci-components.html).

# Parameters

Variables used by this role:

| Setting        | Required | Type   | Description                                                        |
| -------------- | -------- | ------ | -------------------------------------------------------------------|
| ic_rpms        | False    | List   | Optional. List of RPM names to include as components                         |
| ic_gits        | True     | List   | Mandatory. List of directories from GIT repositories to include as components |
| ic_dev_gits    | True     | List   | Mandatory. List of complimentary directories from GIT repositories to include as components |
| ic_repo_commits | False    | List | Optional. List of URLs pointing directly to code commits `[https://github.com/organisation/reponame/commit/b6bcc3506c0d84baa0c020f6b776a181b931f57a, https://github.com/redhat-openshift-ecosystem/openshift-preflight/commit/b6bcc3506c0d84baa0c020f6b776asfasfasdfa]` to include as components. The supported URL formatting is `https://github.com/organisation/reponame/commit/commit_hash`. |

# Examples

```
- name: Create a Git component providing code source dir
  ansible.builtin.include_role:
    name: redhatci.ocp.include_components
  vars:
    ic_gits:
      - "{{ code_source_dir }}"
    ic_dev_gits: []
```

```
- name: Create a component providing repo_url and commit_id
  ansible.builtin.include_role:
  name: redhatci.ocp.include_components
  vars:
    ic_repo_commits:
      - "https://github.com/my-organisation/my-reponame/commit/b6bcc3506c0d84baa0c020f6b776a181b931f57a"
      - "https://github.com/redhat-openshift-ecosystem/openshift-preflight/commit/b6bcc3506c0d84baa0c020f6b776asfasfasdfa"
    ic_gits: []
    ic_dev_gits: []
```
