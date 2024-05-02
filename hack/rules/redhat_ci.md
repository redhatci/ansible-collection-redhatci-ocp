# redhat-ci

This rule checks for compliance with some coding conventions in the OCP
collection

The `redhat-ci` rule has the following checks:

- `redhat-ci[no-role-prefix]` - Variables used within a role should have a
  prefix related to the role. This includes:
  1. Variables passed to `{include,import}_role` and `{include_import}_tasks`
     should be named `$prefix_$var`
  1. Facts saved from within roles should be named `$prefix_$fact`
  1. Variables registered from tasks to use in subsequent tasks should be named
     `_$prefix_$var` - notice the extra underscore to signal this variable is
     "private"

  The rules to figure out the prefix are:
  1. If the role name is $SHORT (where $SHORT is < 6 characters) use the whole
     name
  1. If not, split the role name by underscores into words
  1. If there's a single word, use the first $SHORT characters
  1. Finally, if there are 2 or more words, build an acronym from the split
     words
  1. It is also possible to specify the full prefix of the role (doesn't matter
     if it's "too long") or prefix it with `global_` if the variable is
     intended for global scope.

  Examples of valid prefixes:

  | Role Name               | Prefix        |
  |-------------------------|---------------|
  | `sno`                   | `sno_`        |
  | `installer`             | `insta_`      |
  | `validate_http_store`   | `vhs_`        |
  | `node_prep`             | `node_prep_`  |
  | `provision_registry`    | `global_var`  |

!!! note

    This rule overlaps with the var-naming[no-role-prefix] stock rule, disable
    it in your .ansible-lint config file or by passing a -x flag

## Problematic Code

```yaml
---
- name: Example playbook
  hosts: all
  tasks:
    - name: Include the Node Prep role
      ansible.builtin.include_role:
        name: node_prep
        vars:
          org_id: my_org  # <-- The variable passed does not have a prefix
          my_global_var: some_value  # <-- This variable is "exported"
...
```

## Correct Code

```yaml
---
- name: Example playbook
  hosts: all
  tasks:
    - name: Include the Node Prep role
      ansible.builtin.include_role:
        name: node_prep
        vars:
          np_org_id: my_org  # <-- Variable has a prefix related to the role
          global_var: some_value  # <-- Variable is correctly identified as global
...
```
