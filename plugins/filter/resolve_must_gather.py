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

DOCUMENTATION = r"""
    name: resolve_must_gather
    version_added: "2.10"
    short_description: Resolve must-gather image short names from CSV relatedImages
    description:
        - Takes a list of must-gather image entries and resolves short names
          (e.g. "ptp-must-gather") to full image references using the
          relatedImages from installed ClusterServiceVersion resources.
        - Entries that already contain a "/" are treated as full image
          references and passed through unchanged.
        - Short names are matched against the relatedImages name field
          using substring search.
    positional: _input, related_images
    options:
        _input:
            description: >
                List of must-gather image entries. Each entry is either a full
                image reference (containing "/") or a short name to resolve.
            type: list
            elements: str
            required: true
        related_images:
            description: >
                List of relatedImages dicts from ClusterServiceVersion
                resources. Each dict must have "name" and "image" keys.
            type: list
            elements: dict
            required: true
"""

EXAMPLES = r"""
    # Resolve must-gather short names from CSV relatedImages
    - name: Resolve must-gather images
      ansible.builtin.set_fact:
        resolved_images: >-
          {{ image_list | redhatci.ocp.resolve_must_gather(related_images) }}
      vars:
        image_list:
          - "ose-must-gather"
          - "ptp-must-gather"
          - "registry.redhat.io/openshift4/custom-image:v4.18"
        related_images:
          - name: "ptp-must-gather-rhel9"
            image: "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:abc123"
          - name: "ose-must-gather"
            image: "registry.redhat.io/openshift4/ose-must-gather@sha256:def456"
"""

RETURN = r"""
    _value:
        description: >
            List of resolved image references. Short names are replaced with
            the full image reference from relatedImages. Unresolved short names
            are kept as-is and a warning is emitted.
        type: list
        elements: str
"""


def resolve_must_gather(image_list, related_images):
    """Resolve must-gather image short names from CSV relatedImages.

    Args:
        image_list (list): List of image entries (short names or full refs).
        related_images (list): List of dicts with "name" and "image" keys
            from ClusterServiceVersion relatedImages.

    Returns:
        list: Resolved image references.
    """
    if not isinstance(image_list, list):
        return image_list

    if not isinstance(related_images, list):
        return image_list

    resolved = []
    for entry in image_list:
        if not isinstance(entry, str):
            resolved.append(entry)
            continue

        # Full image reference: pass through
        if "/" in entry:
            resolved.append(entry)
            continue

        # Short name: search in relatedImages
        # Normalize hyphens/underscores for comparison since CSV names
        # may use either style (e.g. "must_gather_image" vs "must-gather")
        entry_normalized = entry.lower().replace("-", "_")
        match = None
        for ri in related_images:
            ri_name = ri.get("name", "").lower().replace("-", "_")
            if entry_normalized in ri_name:
                match = ri.get("image", "")
                break

        if match:
            resolved.append(match)
        else:
            # Keep original so the caller can decide what to do
            resolved.append(entry)

    return resolved


class FilterModule(object):
    def filters(self):
        return {
            "resolve_must_gather": resolve_must_gather,
        }
