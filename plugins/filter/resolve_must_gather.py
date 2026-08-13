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

DOCUMENTATION = r"""
    name: resolve_must_gather
    version_added: "4.3.0"
    short_description: Resolve a must-gather short name to a full image reference
    description:
        - Given a short name (e.g. C(must-gather) or C(oc_must_gather)) and a list
          of fully-qualified image references, returns the first image whose last
          path segment matches the normalised short name.
        - Normalisation converts hyphens and slashes to underscores and lowercases
          the result.  This makes C(must-gather) and C(must_gather) equivalent.
        - Returns an empty string when no match is found.
    positional: _input
    options:
        _input:
            description: Short name of the must-gather image to look up.
            type: str
            required: true
        image_list:
            description: >
              List of fully-qualified image references to search.
              Each entry may be a plain tag reference (C(registry/repo/image:tag))
              or a digest-pinned reference (C(registry/repo/image@sha256:...)).
            type: list
            elements: str
            required: true
"""

EXAMPLES = r"""
    - name: Resolve must-gather image from related images
      ansible.builtin.set_fact:
        mg_image: "{{ 'must-gather' | redhatci.ocp.resolve_must_gather(csv_images) }}"
"""

RETURN = r"""
    _value:
        description: >
          The first matching image reference from I(image_list), or an empty
          string if no match is found.
        type: str
"""


def _normalize(name):
    """Normalise a name for comparison: lower-case, replace '-' and '/' with '_'."""
    return name.replace("-", "_").replace("/", "_").lower()


def resolve_must_gather(short_name, image_list):
    """
    Return the first image in image_list whose last path segment matches short_name.

    Args:
        short_name (str): Short name to look up (e.g. 'must-gather').
        image_list (list): List of fully-qualified image references.

    Returns:
        str: First matching image reference, or '' if not found.
    """
    normalised_target = _normalize(short_name)

    for image in image_list:
        # Strip digest or tag to get the repository path
        # e.g. registry.io/org/must-gather@sha256:abc -> registry.io/org/must-gather
        # e.g. registry.io/org/must-gather:latest    -> registry.io/org/must-gather
        repo_part = image.split("@")[0].split(":")[0]
        # Take the last path segment
        last_segment = repo_part.rstrip("/").rsplit("/", 1)[-1]
        if _normalize(last_segment) == normalised_target:
            return image

    return ""


class FilterModule(object):
    def filters(self):
        return {
            "resolve_must_gather": resolve_must_gather,
        }
