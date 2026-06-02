#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: find_available_port
short_description: Find an available port in a given range
description:
  - Finds an unused port by attempting to bind a socket on a random port
    within the specified range.
  - Supports TCP and UDP protocols. Port spaces are independent per protocol.
  - Supports IPv4 and IPv6 address families.
author:
  - Jose Alberto Rodriguez (@betoredhat)
  - Tony Garcia (@tonyskapunk)
options:
  range_start:
    description:
      - The start of the port range to search.
    required: false
    type: int
    default: 32768
  range_end:
    description:
      - The end of the port range to search (inclusive).
    required: false
    type: int
    default: 60999
  address_family:
    description:
      - The address family to use when checking port availability.
      - Use C(ipv4) to bind on IPv4 or C(ipv6) to bind on IPv6.
    required: false
    type: str
    default: ipv4
    choices:
      - ipv4
      - ipv6
  protocol:
    description:
      - The transport protocol to check port availability for.
      - TCP and UDP have independent port spaces, so a port may be
        available on one protocol but not the other.
    required: false
    type: str
    default: tcp
    choices:
      - tcp
      - udp
  max_attempts:
    description:
      - Maximum number of random ports to try before giving up.
    required: false
    type: int
    default: 100
"""

EXAMPLES = """
- name: Find an available ephemeral port
  redhatci.ocp.find_available_port:
  register: available_port

- name: Use the port
  ansible.builtin.debug:
    msg: "Using port {{ available_port.port }}"

- name: Find a port in a custom range
  redhatci.ocp.find_available_port:
    range_start: 8000
    range_end: 9000
  register: custom_port

- name: Find an available port on IPv6
  redhatci.ocp.find_available_port:
    address_family: ipv6
  register: ipv6_port

- name: Find an available UDP port
  redhatci.ocp.find_available_port:
    protocol: udp
  register: udp_port
"""

RETURN = """
port:
  description: The available port found.
  type: int
  returned: always
  sample: 45123
"""

import random
import socket

from ansible.module_utils.basic import AnsibleModule

ADDRESS_FAMILIES = {
    "ipv4": (socket.AF_INET, ""),
    "ipv6": (socket.AF_INET6, "::"),
}

PROTOCOLS = {
    "tcp": socket.SOCK_STREAM,
    "udp": socket.SOCK_DGRAM,
}


def find_port(
    range_start, range_end, address_family="ipv4", protocol="tcp", max_attempts=100
):
    af, bind_addr = ADDRESS_FAMILIES[address_family]
    sock_type = PROTOCOLS[protocol]
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        port = random.randint(range_start, range_end)
        try:
            s = socket.socket(af, sock_type)
            s.bind((bind_addr, port))
            s.close()
            return port
        except OSError:
            continue
    return None


def main():
    module_args = dict(
        range_start=dict(type="int", required=False, default=32768),
        range_end=dict(type="int", required=False, default=60999),
        address_family=dict(
            type="str",
            required=False,
            default="ipv4",
            choices=["ipv4", "ipv6"],
        ),
        protocol=dict(
            type="str",
            required=False,
            default="tcp",
            choices=["tcp", "udp"],
        ),
        max_attempts=dict(type="int", required=False, default=100),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    range_start = module.params["range_start"]
    range_end = module.params["range_end"]

    if range_start > range_end:
        module.fail_json(
            msg="range_start (%d) must be less than or equal to range_end (%d)"
            % (range_start, range_end)
        )

    if range_start < 1 or range_end > 65535:
        module.fail_json(msg="Port range must be between 1 and 65535")

    address_family = module.params["address_family"]
    protocol = module.params["protocol"]
    max_attempts = module.params["max_attempts"]

    if max_attempts < 1:
        module.fail_json(msg="max_attempts must be at least 1")

    port = find_port(range_start, range_end, address_family, protocol, max_attempts)
    if port is None:
        module.fail_json(
            msg="Could not find an available port in range %d-%d after %d attempts"
            % (range_start, range_end, max_attempts)
        )

    module.exit_json(changed=False, port=port)


if __name__ == "__main__":
    main()
