# etcd data

The `etcd data` role allows to query, encrypt or decrypt etcd data using the supported encryption types.

By default etcd data is not encrypted in OpenShift Container Platform. This role takes care of encrypting/decrypting etcd data.

More info is available at [Encrypting etcd data OpenShift Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/security_and_compliance/encrypting-etcd#about-etcd_encrypting-etcd)

> [!WARNING]:
> - The etcd encryption might affect the memory consumption of a few resources.
> - You might notice a transient affect on backup performance because the leader must serve the backup.
> - A disk I/O can affect the node that receives the backup state.

## Requirements

A valid *KUBECONFIG* env variable pointing to a kubeconfig file.

## Variables

| Variable    | Default    | Required  | Description
| ----------- | ---------- | --------- | -----------
| ed_action   | query      | No        | Action to perform to etcd data (encrypt, decrypt, or query).
| ed_enc      | aesgcm     | No        | Encryption type to use (aesgcm or aescbc).
| ed_force    | false      | No        | Whether or not force the encrypt or decrypt action.

> [!NOTE]
> aesgcm is supported only in OCP 4.13 and above.
> aescbc is the only type supported in OCP 4.12.

### Encryption types

- AES-CBC (aescbc) - Uses AES-CBC with PKCS#7 padding and a 32 byte key to perform the encryption.
- AES-GCM (aesgcm) - Uses AES-GCM with a random nonce and a 32 byte key to perform the encryption.

> [!NOTE]
> The encryption keys are rotated weekly.

## Outputs

- `ed_result`: The state of the etcd data, `encrypted` or `unencrypted` and its type of encryption, when encrypted.

Examples:

- Encrypted:

```yaml
ed_result:
  status: encrypted
  type: aesgcm
```

- Unencrypted:

```yaml
ed_result:
  status: unencrypted
```

## Examples

- Query the etcd data in an OCP cluster

```YAML
- name: Query etcd data
  ansible.builtin.include_role:
    name: redhatci.ocp.etcd_data
  vars:
    ed_action: query

- name: Print etcd data status
  debug:
    var: ed_result
```

- Encrypts the etcd data in an OCP 4.12 cluster

```YAML
- name: Encrypt etcd 
  ansible.builtin.include_role:
    name: redhatci.ocp.etcd_data
  vars:
    ed_action: encrypt
    ed_enc: aescbc
```

- Decrypts the etcd data in an OCP cluster

```YAML
- name: Encrypt etcd 
  ansible.builtin.include_role:
    name: redhatci.ocp.etcd_data
  vars:
    ed_action: decrypt
```
