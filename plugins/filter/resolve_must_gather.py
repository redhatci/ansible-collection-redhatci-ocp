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
        - Short names are matched against both the relatedImages name
          field and the image path using substring search. When the
          entry does not contain "must-gather", matches are restricted
          to relatedImages whose name or path contains "must-gather",
          so generic keywords like "openshift-gitops" or "acm" resolve
          to the correct must-gather image.
    positional: _input, related_images, fallback_registry
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
        fallback_registry:
            description: >
                Registry prefix used when a short name cannot be resolved from
                any CSV relatedImages. Core OCP images (e.g. ose-must-gather)
                are not shipped by any operator CSV and therefore never appear
                in relatedImages. When non-empty, unresolved short names are
                prefixed with this value (e.g. "registry.redhat.io/openshift4"
                resolves "ose-must-gather" to
                "registry.redhat.io/openshift4/ose-must-gather"). Set to an
                empty string to restore the original behaviour of keeping the
                short name as-is.
            type: str
            default: ""
"""

EXAMPLES = r"""
    # Resolve must-gather short names from CSV relatedImages
    - name: Resolve must-gather images
      ansible.builtin.set_fact:
        resolved_images: >-
          {{ image_list | redhatci.ocp.resolve_must_gather(related_images) }}
      vars:
        image_list:
          - "ptp-must-gather"
          - "registry.redhat.io/openshift4/custom-image:v4.18"
        related_images:
          - name: "ptp-must-gather-rhel9"
            image: "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:abc123"

    # Resolve with fallback registry for core OCP images (not in any CSV)
    - name: Resolve must-gather images with fallback for core OCP images
      ansible.builtin.set_fact:
        resolved_images: >-
          {{ image_list
             | redhatci.ocp.resolve_must_gather(related_images,
                                                'registry.redhat.io/openshift4') }}
      vars:
        image_list:
          - "ose-must-gather"
          - "ptp-must-gather"
          - "registry.redhat.io/openshift4/custom-image:v4.18"
        related_images:
          - name: "ptp-must-gather-rhel9"
            image: "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:abc123"
"""

RETURN = r"""
    _value:
        description: >
            List of resolved image references. Short names are replaced with
            the full image reference from relatedImages. Unresolved short names
            are kept as-is.
        type: list
        elements: str
"""


def _extract_rhel_suffix(image_ref):
    """Extract the RHEL suffix (e.g. '-rhel8', '-rhel9') from an image ref.

    Looks at the image path component (before any @sha256: or :tag) for
    a '-rhel[0-9]+' pattern.
    """
    import re
    path = image_ref.split("@")[0].split(":")[0]
    basename = path.rsplit("/", 1)[-1]
    m = re.search(r"(-rhel\d+)", basename)
    return m.group(1) if m else ""


def _find_operator_image(keyword, related_images):
    """Find a relatedImage whose name or image path contains the keyword."""
    kw = keyword.lower().replace("-", "_")
    for ri in related_images:
        ri_name = ri.get("name", "").lower().replace("-", "_")
        ri_image = ri.get("image", "")
        ri_path = ri_image.split("@")[0].split(":")[0].rsplit("/", 1)[-1]
        ri_path_norm = ri_path.lower().replace("-", "_")
        if kw in ri_name or kw in ri_path_norm:
            return ri_image
    return ""


def resolve_must_gather(image_list, related_images, fallback_registry=""):
    """Resolve must-gather image short names from CSV relatedImages.

    Args:
        image_list (list): List of image entries (short names or full refs).
        related_images (list): List of dicts with "name" and "image" keys
            from ClusterServiceVersion relatedImages.
        fallback_registry (str): Registry prefix used when a short name cannot
            be resolved from any CSV relatedImages. Core OCP images (e.g.
            ose-must-gather) are not shipped by any operator CSV and therefore
            never appear in relatedImages. When non-empty, unresolved short
            names are prefixed with this value. Defaults to "" (keep as-is).

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

        # Short name: search in relatedImages by name and image path.
        # When the entry doesn't already contain "must_gather", restrict
        # matches to relatedImages whose name or image path does — so
        # generic keywords like "openshift-gitops" or "acm" only match
        # must-gather images, not arbitrary operator images.
        entry_normalized = entry.lower().replace("-", "_")
        is_mg_entry = "must_gather" in entry_normalized
        match = None
        for ri in related_images:
            ri_name = ri.get("name", "").lower().replace("-", "_")
            ri_image = ri.get("image", "")
            ri_path = ri_image.split("@")[0].split(":")[0].lower().replace("-", "_")
            if entry_normalized in ri_name or entry_normalized in ri_path:
                if is_mg_entry or "must_gather" in ri_name or "must_gather" in ri_path:
                    match = ri_image
                    break

        if match:
            resolved.append(match)
        elif fallback_registry:
            # Must-gather images are not in CSV relatedImages.  Try to
            # infer the RHEL suffix from the operator's own images.
            # E.g. for "ptp-must-gather", find an operator image containing
            # "ptp" to discover the "-rhel8" or "-rhel9" suffix.
            rhel_suffix = ""
            keyword = (entry_normalized
                       .replace("must_gather", "")
                       .replace("ose_", "")
                       .strip("_"))
            if keyword:
                op_image = _find_operator_image(keyword, related_images)
                if op_image:
                    rhel_suffix = _extract_rhel_suffix(op_image)
            resolved.append(
                "{0}/{1}{2}".format(fallback_registry, entry, rhel_suffix))
        else:
            # Keep original so the caller can decide what to do
            resolved.append(entry)

    return resolved


class FilterModule(object):
    def filters(self):
        return {
            "resolve_must_gather": resolve_must_gather,
        }
