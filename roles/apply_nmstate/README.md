# apply_nmstate

Applies nmstate network configuration to a host.

## Variables

| Variable                 | Default  | Required             | Description                        |
| ------------------------ | -------- | -------------------- | ---------------------------------- |
| rendered_nmstate_yml     | -        | Yes                  | The nmstate to apply               |
| vm_nmstate_config_path   | -        | Yes                  | The path to place the nmstate file |
| vm_network_test_ip       | -        | Depends on the host  | An IP to check outbound connectivity post application. This is required host is the ansible control node. |
