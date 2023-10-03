# merge_registry_creds role

A Role to combine multiple registry credentials in JSON format passed as dictionaries. The list of credentials is processed in order, in case of duplicated entries the last one processed will take precedence.

## Parameters

Name             | Required | Default        | Description
-----------------|----------| ---------------|-------------
mrc_auths        | Yes      |                | A list of dictionaries containing authentication entries that will be merged

## Outputs

The `mrc_auth_file` variable points to the file can be used directly in images mirroring or inspection tools that support the JSON auths format.

The `mrc_auth_data` variable contains the result of combining all the authentication files.

## Example of usage

```yaml
- name: "Combine registry auth secrets"
  include_role:
    name: merge_registry_creds
  vars:
    mrc_auths:
      - auths:
          quay.io:
            auth: "XXXX"
          cloud.openshift.com:
            auth: "YYYY",
            email: "someone@example.com"
      - auths:
          docker.io:
            auth: "ZZZZ"
          quay.io/ns:
            auth: "AAAA"
```
