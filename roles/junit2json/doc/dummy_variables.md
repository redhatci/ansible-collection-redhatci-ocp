# Template Handling in junit2json Role

## The Problem

Test data sometimes contains literal strings that look like Jinja2 templates:

```xml
<testcase name="... expectations failed: {{ expectation_failed }}" />
<testcase name="... log at: https://ci.example.com/jobs/{{ job_info.job.id }}/states" />
```

When Ansible processes this data, it tries to evaluate these as templates, causing:
```
ERROR! 'expectation_failed' is undefined
ERROR! 'job_info' is undefined
```

## The Solution

The role provides dummy variables for template patterns. Which method you use depends on **variable frequency** and **your maintenance access**:

## Adding Dummy Variables

### High Frequency Variables (appear across many teams/projects)

**If you maintain the role:**
Edit `vars/dummy_variables.yml`:

```yaml
junit2_dummy_variables:
  # Add variables that many teams encounter
  common_variable: "PLACEHOLDER_COMMON_VARIABLE"
  shared_info:
    build_id: "PLACEHOLDER_BUILD_ID"
```

**If you don't maintain the role:**
Request the role maintainer to add these variables to `vars/dummy_variables.yml`.

### Low Frequency Variables (specific to your team/project)

**If you maintain the playbook:**
Add variables when calling the role:

```yaml
- name: Convert test reports
  ansible.builtin.include_role:
    name: redhatci.ocp.junit2json
  vars:
    junit2_custom_dummy_variables:
      # Add team-specific variables
      pipeline_id: "PLACEHOLDER_PIPELINE_ID"
      deployment:
        environment: "PLACEHOLDER_ENVIRONMENT"
```

**If you don't maintain the playbook:**
Create an external variables file `my_extras.yml`:

```yaml
junit2_custom_dummy_variables:
  pipeline_id: "PLACEHOLDER_PIPELINE_ID"
  deployment:
    environment: "PLACEHOLDER_ENVIRONMENT"
```

Run with:
```shell
ansible-playbook my_playbook.yml -e @my_extras.yml
```

### Debug Mode

Enable debug to see what variables are being set:

```yaml
junit2_dummy_debug: true
```

## Role Maintenance & Feedback

**This role is maintained by:** GitHub team `@redhatci/verification`

**Help us improve:** Please share your custom dummy variables with the maintenance team! When you add variables using `junit2_custom_dummy_variables` or external files, let `@redhatci/verification` know what variables you needed. This helps us identify high-frequency variables that should be moved into the role for everyone's benefit.

## Variables Already Handled

These patterns are already handled (may change based on test data encountered):

- `{{ expectation_failed }}`
- `{{ job_info.job.id }}`
- `{{ ci_job_id }}`
- `{{ error_message }}`
- `{{ timestamp }}` 