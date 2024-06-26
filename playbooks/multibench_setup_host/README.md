# Multi-bench playbook

## Variables

| Variable                  | Default                        | Type    | Required | Description                                                                          |
|---------------------------|--------------------------------|---------|----------|--------------------------------------------------------------------------------------|
| multibench_quay_token     | null                           | string  | true     | Path to the file which contains the credentials for accessing the container registry |
| multibench_disconnected   | false                          | boolean | false    | Set it to 'true' if the multibench host does not have access to the Internet         |
| multibench_local_registry | quay.io/crucible/client-server | String  | false    | Registry that will be used to pull the crucible images                               |
| multibench_git_name       | Smith                          | String  | false    | Name displayed in on git                                                             |
| multibench_git_email      | ansible@whatever.com           | String  | false    | email displayed in on git                                                            |

## Requirements
The playbook will be run on the host `multibench`, make sure it is correctly defined in your inventory, here is an example:
```yaml
  children:
    multibench:
      hosts:
        my-host.my-lab:
          ansible_user: root
```
Also, the installation needs to be run as root, verify that the ansible_user is correctly set.
