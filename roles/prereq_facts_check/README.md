# Prereqs facts check

Checks that required facts are set correctly

## Role Variables

- `pull_secret_check`: Wether to check `pull_secret` fact is valid
- `ssh_public_check`: Wether to check `ssh_public` fact is valid
- `mirror_certificate_check`: Wether to check `mirror_certificate` fact is valid

## Example Playbook

```yaml
- name: Check facts
  hosts: localhost
  roles:
    - prereq_facts_check
```
