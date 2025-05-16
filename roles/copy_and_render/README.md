# copy_and_render

Role to copy files and subdirectories from a source directory to a target directory, then render and replace all Jinja2 `.j2` templates.

Role Variables:

`car_source_dir` (string, required): Source directory on the control machine containing files and `.j2` templates.
`car_target_dir` (string, required): Destination directory on the remote host where files will be copied and templates rendered.

Example Playbook:

```yaml
- hosts: all
  roles:
    - role: copy_and_render
      vars:
        car_source_dir: "/path/to/source"
        car_target_dir: "/path/to/target"
```

Requirements:

- Ansible 2.9 or higher

License:

Apache-2.0
