# Copyright 2025 Red Hat, Inc.
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

import copy

DOCUMENTATION = r"""
    name: redact
    version_added: "2.10"
    short_description: Redact sensitive values from dictionary keys
    description:
        - Redacts sensitive values from a dictionary by replacing them with "REDACTED".
        - Matches keys case-insensitively against a comma-separated list of field names.
    positional: _input
    options:
        _input:
            description: The dictionary containing potentially sensitive data to be redacted.
            type: dict
            required: true
        fields:
            description: Comma-separated string of key names to redact. Keys are matched case-insensitively.
            type: str
            required: false
            default: "auth,api_secret,password"
"""

EXAMPLES = r"""
    - name: redact
      ansible.builtin.debug:
        var:  dictionary | redact(fields="auth,token,password")
"""

RETURN = r"""
    _value:
        description: The dictionary with redacted fields
        type: dict
"""


def redact(data, fields="auth,api_secret,password"):
    """
    Redact sensitive information from a dictionary.

    Args:
        data (dict): Dictionary containing potentially sensitive data
        fields (str): Comma-separated string of field names to redact (case-insensitive)

    Returns:
        dict: Dictionary with specified fields redacted as "REDACTED"
    """
    redacted = {}
    fields = [f.strip().lower() for f in fields.split(",")]

    if not isinstance(data, dict):
        return data

    def redact_fields(d):
        for key, value in d.items():
            if key.lower() in fields:
                d[key] = "REDACTED"
            elif isinstance(value, dict):
                redact_fields(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        redact_fields(item)
        return d

    data_copy = copy.deepcopy(data)
    redacted = redact_fields(data_copy)

    return redacted


class FilterModule(object):
    def filters(self):
        return {
            "redact": redact,
        }
