# forgejo_config

A role to configure an already deployed Forgejo Git service instance.

## Description

This role configures a Forgejo instance by managing:
- User accounts
- Organizations with member permissions
- Repositories (user-owned or organization-owned)
- SSH keys (existing or generated on demand)

This role is designed to work with a Forgejo instance deployed by the `forgejo_setup` role or any other Forgejo deployment method.

## Requirements

- A running Forgejo instance accessible via HTTP/HTTPS
- Admin credentials for the Forgejo instance
- Ansible collection: [community.crypto](https://galaxy.ansible.com/community/crypto) (for SSH key generation)

## Role Variables

### Connection Settings

| Variable          | Default               | Required | Description
| --------          | -------               | -------- | -----------
| fc_url            | http://localhost:3000 | Yes      | URL to the Forgejo instance
| fc_admin_user     | forgejo               | Yes      | Admin username for API authentication
| fc_admin_password | ""                    | Yes      | Admin password for API authentication

### User Management

| Variable | Default | Required | Description
| -------- | ------- | -------- | -----------
| fc_users | []      | Yes      | List of users to create (see example below)

User object structure:
```yaml
- username: string            # Required: Username
  email: string               # Required: Email address
  password: string            # Required: User password
  full_name: string           # Optional: Full name (defaults to username)
  must_change_password: bool  # Optional: Force password change on first login (default: false)
  send_notify: bool           # Optional: Send notification email (default: false)
```

### Organization Management

| Variable  | Default | Required | Description
| --------  | ------- | -------- | -----------
| fc_orgs   | []      | Yes      | List of organizations to create (see example below)

Organization object structure:
```yaml
- name: string             # Required: Organization name
  full_name: string        # Optional: Full organization name (defaults to name)
  description: string      # Optional: Organization description
  visibility: string       # Optional: public or private (default: public)
  members:                 # Optional: List of members to add
    - username: string     # Required: Username to add
      role: string         # Optional: owner or member (default: member)
```

#### Organization Team Management

When an organization is created, the role automatically manages two teams:

1. **Owners Team**: Automatically created by Forgejo when the organization is created. This team has admin permissions on all organization repositories.

2. **Members Team**: Created by the role with the following permissions:
   - `repo.code` - Read access to code
   - `repo.issues` - Read access to issues
   - `repo.pulls` - Read access to pull requests
   - `repo.releases` - Read access to releases
   - `repo.wiki` - Read access to wiki

**Member Assignment Rules**:
- Members with `role: owner` are added to the **Owners team**
- Members with `role: member` or **no role defined** are added to the **Members team**
- If no role is specified, the default is `member`

**Example**:
```yaml
fc_orgs:
  - name: engineering
    members:
      - username: alice
        role: owner        # Added to Owners team
      - username: bob
        role: member       # Added to Members team
      - username: charlie  # No role specified - added to Members team (default)
```

### Repository Management

| Variable        | Default | Required | Description
| --------        | ------- | -------- | -----------
| fc_repositories | []      | Yes      | List of repositories to create (see example below)

Repository object structure:
```yaml
- name: string             # Required: Repository name
  owner: string            # Required: Username or organization name
  description: string      # Optional: Repository description
  private: bool            # Optional: Private repository (default: true)
  auto_init: bool          # Optional: Initialize with README (default: false)
  default_branch: string   # Optional: Default branch name (default: main)
  gitignores: string       # Optional: Gitignore template
  license: string          # Optional: License template
  readme: string           # Optional: README template
  template: bool           # Optional: Is template repository (default: false)
  trust_model: string      # Optional: Trust model (default: default)
```

### SSH Key Management

| Variable    | Default | Required | Description
| --------    | ------- | -------- | -----------
| fc_ssh_keys | []      | Yes      | List of SSH keys to manage (see example below)

SSH key object structure:
```yaml
- username: string         # Required: Username to add key for
  title: string            # Optional: Key title/label (default: "SSH Key")
  generate: bool           # Optional: Generate new key pair (default: false)
  priv_key: string         # Optional: Path to save generated private key (required if generate is true)
  pub_key: string          # Optional: Path to read a provided public key
  read_only: bool          # Optional: Read-only key (default: false)
```

### Behavior Settings

| Variable       | Default | Required | Description
| --------       | ------- | -------- | -----------
| fc_api_retries | 3       | No       | Number of API call retries
| fc_api_delay   | 2       | No       | Delay in seconds between retries

## Dependencies

- community.crypto collection (for SSH key generation)

## Usage Examples

### Basic Configuration with Users and Repositories

```yaml
- name: Configure Forgejo instance
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_config
  vars:
    fc_url: "http://localhost:3000"
    fc_admin_user: forgejo
    fc_admin_password: "AdminPass123"
    fc_users:
      - username: developer1
        email: developer1@example.com
        password: "DevPass123"
        full_name: "Developer One"
      - username: developer2
        email: developer2@example.com
        password: "DevPass456"
        full_name: "Developer Two"
    fc_repositories:
      - name: myproject
        owner: developer1
        description: "My awesome project"
        private: false
        auto_init: true
```

### Create Organization with Members and Repositories

```yaml
- name: Setup organization with team
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_config
  vars:
    fc_url: "http://localhost:3000"
    fc_admin_user: forgejo
    fc_admin_password: "AdminPass123"
    fc_users:
      - username: teamlead
        email: teamlead@example.com
        password: "LeadPass123"
      - username: developer1
        email: developer1@example.com
        password: "DevPass123"
      - username: developer2
        email: developer2@example.com
        password: "DevPass456"
    fc_orgs:
      - name: myteam
        full_name: "My Development Team"
        description: "Our awesome development team"
        visibility: public
        members:
          - username: teamlead
            role: owner
          - username: developer1
            role: member
          - username: developer2
            role: member
    fc_repositories:
      - name: team-project
        owner: myteam
        description: "Team project repository"
        private: true
        auto_init: true
        default_branch: main
```

### Manage SSH Keys for Users

```yaml
- name: Add SSH keys for developers
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_config
  vars:
    fc_url: "http://localhost:3000"
    fc_admin_user: forgejo
    fc_admin_password: "AdminPass123"
    fc_ssh_keys:
      # Add existing SSH key
      - username: developer1
        title: "Developer 1 Workstation"
        pub_key: "/path/to/key.pub"
      # Generate new SSH key pair
      - username: developer2
        title: "Developer 2 Generated Key"
        generate: true
        priv_key: "/tmp/developer2_id_ed25519"
```

### Complete Setup Example

```yaml
- name: Complete Forgejo configuration
  ansible.builtin.include_role:
    name: redhatci.ocp.forgejo_config
  vars:
    fc_url: "http://forgejo.example.com"
    fc_admin_user: forgejo
    fc_admin_password: "{{ vault_forgejo_admin_password }}"
    fc_users:
      - username: alice
        email: alice@example.com
        password: "{{ vault_alice_password }}"
        full_name: "Alice Developer"
      - username: bob
        email: bob@example.com
        password: "{{ vault_bob_password }}"
        full_name: "Bob Developer"
    fc_orgs:
      - name: engineering
        full_name: "Engineering Team"
        description: "Main engineering organization"
        visibility: private
        members:
          - username: alice
            role: owner
          - username: bob
            role: member
    fc_repositories:
      - name: backend-api
        owner: engineering
        description: "Backend API service"
        private: true
        auto_init: true
      - name: frontend-app
        owner: engineering
        description: "Frontend application"
        private: true
        auto_init: true
    fc_ssh_keys:
      - username: alice
        title: "Alice Work Key"
        pub_key: "/path/to/alice_key.pub"
      - username: bob
        title: "Bob Laptop Key"
        generate: true
        priv_key: "/path/to/generated_bob_key"
```

## Notes

- The role uses the Forgejo API v1, which is compatible with the Gitea API
- SSH key generation requires the `community.crypto` collection
- All API operations are idempotent and can be safely re-run
- Existing resources are skipped if already present.
- Sensitive information (passwords, keys) is marked with `no_log` to prevent logging

## References

- [Forgejo Documentation](https://forgejo.org/docs/)
- [Forgejo API Documentation](https://forgejo.org/docs/latest/user/api-usage/)
- [forgejo_setup role](../forgejo_setup/) - Deploy Forgejo instance
