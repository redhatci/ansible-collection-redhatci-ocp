# setup_ksops

Installs and sets up the KSOPS Kustomize plugin on the OpenShift GitOps Operator.

## Variables

| Variable         | Default | Required | Description
| ---------------- | ------- | -------- | -----------
| sk_age_key       |         | yes      | A literal age generated (age-keygen) key. If kept in a version control service, it's recommeneded to vault-encrypt it.

## Example of age key

```
# created: 2025-04-16T11:28:48Z
# public key: age1j24rsa89nhv86dstnl696pfhxlngktjl5gcvya6y6ykg8t5jkqgsv0ua36
AGE-SECRET-KEY-16NSYF9LSS3QZKLXFEYS5K36FPQC62QLZPNA02H7YWV0SFFVXF2PQNRZPNQ
```

## Usage examples

```
- name: Setup the KSOPS Kustomize plugin
  ansible.builtin.include_role:
    name: redhatci.ocp.acm.setup_ksops
  vars:
    sk_age_key: |
      # created: 2025-04-16T11:28:48Z
      # public key: age1j24rsa89nhv86dstnl696pfhxlngktjl5gcvya6y6ykg8t5jkqgsv0ua36
      AGE-SECRET-KEY-16NSYF9LSS3QZKLXFEYS5K36FPQC62QLZPNA02H7YWV0SFFVXF2PQNRZPNQ
```

## How to encrypt the gitops data

Install first the required binaries (age and [sops](https://github.com/getsops/sops/releases)):

```
dnf install age

# Download the sops binary
curl -LO https://github.com/getsops/sops/releases/download/v3.10.2/sops-v3.10.2.linux.amd64

# Move the binary in to your PATH
mv sops-v3.10.2.linux.amd64 /usr/local/bin/sops

# Make the binary executable
chmod +x /usr/local/bin/sops

```

Create a working directory:

```
mkdir sops
cd sops
```

Create an age key:

```
age-keygen -o age.key
```

Define the SOPS creation rules. The age public key is available in the age.key file:

```
cat <<EOF > .sops.yaml
creation_rules:
  - encrypted_regex: "^(data|stringData)$"
    age: age1...< your age public key>
EOF
```

Encrypt your secret files in your local copy of the GitOps repository:

```
sops --encrypt --in-place /path/to/gitops/secret.yaml
```

Add a KSOPS generator to your repository:

```
cat <<EOF > secret-generator.yaml
apiVersion: viaduct.ai/v1
kind: ksops
metadata:
  # Specify a name
  name: secret-generator
files:
  - ./secret.yaml
EOF
```

Include the KSOPS generator in your kustomization file:

```
cat <<EOF > kustomization.yaml
generators:
  - ./secret-generator.yaml
EOF
```

Add the new files to your git repository and commit the changes.