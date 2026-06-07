# Copyright 2026 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from json import dumps

DOCUMENTATION = r"""
    name: cmdline_to_json
    version_added: "2.10"
    short_description: Convert a kernel command line string to a JSON object
    description:
        - Parses a kernel command line string (space-separated key=value pairs)
          and returns a JSON string representation.
        - Handles bare flags (tokens without C(=)) by assigning them an empty
          string value.
        - Splits comma-separated values into lists, except for the C(BOOT_IMAGE) key.
        - Supports dot-separated keys to create nested dictionary structures.
    positional: _input
    options:
        _input:
            description: The kernel command line string to parse.
            type: str
            required: true
"""

EXAMPLES = r"""
    - name: Parse kernel cmdline into JSON
      ansible.builtin.debug:
        msg: "{{ ansible_cmdline_string | redhatci.ocp.cmdline_to_json }}"
"""

RETURN = r"""
    _value:
        description: JSON string representing the parsed kernel command line.
        type: str
"""


def cmdline_to_json(cmdline=""):
    """Convert a kernel command line string to a JSON object.

    Args:
        cmdline (str): The kernel command line string to parse.

    Returns:
        str: A JSON string representing the parsed kernel command line.
    """
    kernel = {}

    for item in cmdline.split():
        if "=" in item:
            k, v = item.split("=", 1)
            # Handle comma-separated values for specific keys
            if "," in v and k not in ["BOOT_IMAGE"]:
                v = v.split(",")
        else:
            k = item
            v = ""

        # Handle nested keys - any key with dots creates nested structure
        if "." in k:
            parts = k.split(".")
            current = kernel
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = v
        else:
            kernel[k] = v

    return dumps(kernel)


class FilterModule(object):
    def filters(self):
        return {
            "cmdline_to_json": cmdline_to_json,
        }
