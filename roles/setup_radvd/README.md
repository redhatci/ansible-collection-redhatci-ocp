# Set Up the Router ADVertisement Daemon (radvd) role

The purpose of this role is to set up an infrastructure host with a basic IPv6 radvd to facilitate
self-management of IPv6 DHCP6 IP address management in a lab subnet.

This requires switch configuration to ensure they are not competing with your infrastructure host to answer requests.

## Variables

All the variables defined are employed exclusively in the radvd.conf Jinja template to create the configuration file.

- `setup_radvd_ipv6_network_cidr` This defines the IPv6 network segment (in CIDR
notation) for which radvd will advertise itself as the default route. No default
is provided and the role will error out if it is undefined.

The remaining variables are provided to allow tweaking of settings. Sane defaults have been set for these.

- `setup_radvd_baremetal_bridge` This defines the interface radvd will listen
on, typically a bridge accessible to libvirt virtual machines and OCP cluster
nodes. Defaults to "baremetal".
- `setup_radvd_min_interval` Default 30 seconds
- `setup_radvd_max_interval` Default 100 seconds
- `setup_radvd_default_lifetime` Default 9000 seconds (2.5 hours)
