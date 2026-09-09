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
    short_description: Resolve must-gather image hints from installed CSVs
    description:
        - Takes a list of must-gather image hints and resolves short names
          (e.g. "ptp", "acm", "gitops") to full image references using
          installed ClusterServiceVersion resources.
        - Full image references (containing "/") are ignored.
        - Matching CSVs are identified from the CSV name, displayName,
          annotations, and relatedImages.
        - The image is taken first from the
          operators.openshift.io/must-gather-image annotation, then from
          other must-gather / mustgather annotations, then from relatedImages.
        - Duplicate resolved images are returned once.
        - Hints that cannot be resolved are omitted from the result.
    positional: _input, csvs
    options:
        _input:
            description: >
                List of must-gather image hints. Each entry is a short name
                or keyword to resolve. Full image references (containing "/")
                are ignored.
            type: list
            elements: str
            required: true
        csvs:
            description: >
                List of CSV lookup dicts. Each dict may have "name",
                "display_name", "annotations", and "related_images" keys.
                related_images is a list of dicts with "name" and "image".
            type: list
            elements: dict
            required: true
"""

EXAMPLES = r"""
    # Resolve must-gather short names from installed CSVs
    - name: Resolve must-gather images
      ansible.builtin.set_fact:
        resolved_images: >-
          {{ image_list | redhatci.ocp.resolve_must_gather(csvs) }}
      vars:
        image_list:
          - "ptp"
          - "acm"
        csvs:
          - name: "ptp-operator.v4.18.0"
            display_name: "PTP Operator"
            annotations:
              operators.openshift.io/must-gather-image: >-
                registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:abc
            related_images: []
"""

RETURN = r"""
    _value:
        description: >
            List of unique resolved image references. Unresolved short names
            are omitted.
        type: list
        elements: str
"""

MG_ANNOTATION = "operators.openshift.io/must-gather-image"
_MIN_TOKEN_LEN = 3


def _norm(value):
    return (value or "").lower().replace("-", "_")


def _looks_like_must_gather(text):
    """True if text looks like a must-gather image name or annotation key."""
    normalized = _norm(text)
    return "must_gather" in normalized or "mustgather" in normalized


def _hint_tokens(hint):
    """Build match tokens from a hint.

    "ptp-must-gather" yields {"ptp_must_gather", "ptp"}.
    Tokens shorter than 3 characters are dropped to avoid accidental matches.
    """
    normalized = _norm(hint)
    tokens = {normalized}
    stripped = (
        normalized.replace("must_gather", "")
        .replace("mustgather", "")
        .strip("_")
    )
    if stripped:
        tokens.add(stripped)
    return {token for token in tokens if len(token) >= _MIN_TOKEN_LEN}


def _normalize_csvs(csvs):
    """Accept CSV lookup dicts or a legacy flat relatedImages list."""
    if not csvs:
        return []
    first = csvs[0]
    if not isinstance(first, dict):
        return []
    if (
        "related_images" in first
        or "annotations" in first
        or "display_name" in first
    ):
        return csvs
    return [
        {
            "name": "",
            "display_name": "",
            "annotations": {},
            "related_images": csvs,
        }
    ]


def _csv_blob(csv):
    parts = [csv.get("name") or "", csv.get("display_name") or ""]
    annotations = csv.get("annotations") or {}
    for key, value in annotations.items():
        parts.append(str(key))
        parts.append(str(value))
    for related in csv.get("related_images") or []:
        if not isinstance(related, dict):
            continue
        parts.append(related.get("name") or "")
        parts.append(related.get("image") or "")
    return _norm(" ".join(parts))


def _csv_matches(csv, tokens):
    blob = _csv_blob(csv)
    return any(token in blob for token in tokens)


def _related_must_gather_image(related_images, tokens):
    related_images = related_images or []
    hint_match = None
    any_mg = None
    for related in related_images:
        if not isinstance(related, dict):
            continue
        name = _norm(related.get("name", ""))
        path = _norm(related.get("image", ""))
        image = related.get("image")
        if not image:
            continue
        if not _looks_like_must_gather(name) and not _looks_like_must_gather(path):
            continue
        if any_mg is None:
            any_mg = image
        if any(token in name or token in path for token in tokens):
            hint_match = image
            break
    return hint_match or any_mg


def _image_from_csv(csv, tokens):
    annotations = csv.get("annotations") or {}
    official = annotations.get(MG_ANNOTATION)
    if official:
        return official
    for key, value in annotations.items():
        if key == MG_ANNOTATION:
            continue
        if _looks_like_must_gather(key) and value and "/" in str(value):
            return value
    return _related_must_gather_image(csv.get("related_images"), tokens)


def _has_official_annotation(csv):
    annotations = csv.get("annotations") or {}
    return bool(annotations.get(MG_ANNOTATION))


def resolve_must_gather(image_list, csvs):
    """Resolve must-gather image short names from installed CSVs.

    Args:
        image_list (list): List of short-name hints (full refs are ignored).
        csvs (list): List of CSV lookup dicts, or a legacy flat relatedImages
            list of {"name", "image"} dicts.

    Returns:
        list: Unique resolved image references. Unresolved short names are omitted.
    """
    if not isinstance(image_list, list):
        return image_list

    if not isinstance(csvs, list):
        return []

    csv_list = _normalize_csvs(csvs)
    resolved = []
    for entry in image_list:
        if not isinstance(entry, str):
            continue

        if "/" in entry:
            continue

        tokens = _hint_tokens(entry)
        if not tokens:
            continue

        matched = [csv for csv in csv_list if _csv_matches(csv, tokens)]
        matched.sort(key=lambda csv: 0 if _has_official_annotation(csv) else 1)
        match = None
        for csv in matched:
            match = _image_from_csv(csv, tokens)
            if match:
                break

        if match and match not in resolved:
            resolved.append(match)

    return resolved


class FilterModule(object):
    def filters(self):
        return {
            "resolve_must_gather": resolve_must_gather,
        }
