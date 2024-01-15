# redhat.ocp.include_components role - create and attach DCI components to the DCI jobs

# Synopsis

The `include_components` role creates and attaches DCI components to the DCI jobs by generating them from provided resources. Possible resource inputs include RPM packages, Git repositories, and Github commits.

Follow this post to know more about [components](https://blog.distributed-ci.io/automate-dci-components.html).

# Parameters

Variables used by this role:

| Setting        | Required | Type   | Description                                                        |
| -------------- | -------- | ------ | -------------------------------------------------------------------|                       |
| ic_gits        | True     | List   | Mandatory. List of directories from GIT repositories to include as components. |
| ic_dev_gits    | True     | List   | Mandatory. List of complimentary directories from GIT repositories to include as components. |
| ic_rpms        | False    | List   | Optional. List of RPM names to include as components.
| ic_commit_urls | False    | List   | Optional. List of Github URLs pointing directly to code commits `[https://github.com/organisation/reponame/commit/b6bcc3506c0d84baa0c020f6b776a181b931f57a, https://github.com/redhat-openshift-ecosystem/openshift-preflight/commit/b6bcc3506c0d84baa0c020f6b776asfasfasdfa]` to include as components. The supported URL formatting is `https://github.com/organisation/reponame/commit/commit_hash` and should contain the full commit hash. |

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
    ic_commit_urls:
      - "https://github.com/my-organisation/my-reponame/commit/b6bcc3506c0d84baa0c020f6b776a181b931f57a"
      - "https://github.com/redhat-openshift-ecosystem/openshift-preflight/commit/b6bcc3506c0d84baa0c020f6b776asfasfasdfa"
    ic_gits: []
    ic_dev_gits: []
```
