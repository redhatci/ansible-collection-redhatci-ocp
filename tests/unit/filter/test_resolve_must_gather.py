#
# Copyright (C) 2025 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible_collections.redhatci.ocp.plugins.filter import resolve_must_gather


SAMPLE_RELATED_IMAGES = [
    {
        "name": "ose-must-gather",
        "image": "registry.redhat.io/openshift4/ose-must-gather@sha256:aaa111",
    },
    {
        "name": "ptp-must-gather-rhel9",
        "image": "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:bbb222",
    },
    {
        "name": "sriov-network-must-gather-rhel9",
        "image": "registry.redhat.io/openshift4/sriov-network-must-gather-rhel9@sha256:ccc333",
    },
    {
        "name": "ptp-operator",
        "image": "registry.redhat.io/openshift4/ptp-operator@sha256:ddd444",
    },
    {
        "name": "linuxptp-daemon-rhel9",
        "image": "registry.redhat.io/openshift4/linuxptp-daemon-rhel9@sha256:eee555",
    },
]


class TestResolveMustGather:
    def test_resolve_short_name(self):
        """Test resolving a short name to a full image reference."""
        result = resolve_must_gather.resolve_must_gather(
            ["ptp-must-gather"], SAMPLE_RELATED_IMAGES
        )
        assert result == [
            "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:bbb222"
        ]

    def test_resolve_multiple_short_names(self):
        """Test resolving multiple short names."""
        result = resolve_must_gather.resolve_must_gather(
            ["ose-must-gather", "ptp-must-gather", "sriov-network-must-gather"],
            SAMPLE_RELATED_IMAGES,
        )
        assert result == [
            "registry.redhat.io/openshift4/ose-must-gather@sha256:aaa111",
            "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:bbb222",
            "registry.redhat.io/openshift4/sriov-network-must-gather-rhel9@sha256:ccc333",
        ]

    def test_passthrough_full_reference(self):
        """Test that full image references are passed through unchanged."""
        full_ref = "registry.redhat.io/openshift4/custom-image:v4.18"
        result = resolve_must_gather.resolve_must_gather(
            [full_ref], SAMPLE_RELATED_IMAGES
        )
        assert result == [full_ref]

    def test_mixed_short_and_full(self):
        """Test mix of short names and full references."""
        result = resolve_must_gather.resolve_must_gather(
            [
                "ose-must-gather",
                "registry.redhat.io/openshift4/custom-image:latest",
                "ptp-must-gather",
            ],
            SAMPLE_RELATED_IMAGES,
        )
        assert result == [
            "registry.redhat.io/openshift4/ose-must-gather@sha256:aaa111",
            "registry.redhat.io/openshift4/custom-image:latest",
            "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:bbb222",
        ]

    def test_unresolved_short_name_kept(self):
        """Test that unresolved short names are kept as-is."""
        result = resolve_must_gather.resolve_must_gather(
            ["nonexistent-must-gather"], SAMPLE_RELATED_IMAGES
        )
        assert result == ["nonexistent-must-gather"]

    def test_empty_image_list(self):
        """Test with an empty image list."""
        result = resolve_must_gather.resolve_must_gather([], SAMPLE_RELATED_IMAGES)
        assert result == []

    def test_empty_related_images(self):
        """Test with empty relatedImages list."""
        result = resolve_must_gather.resolve_must_gather(
            ["ptp-must-gather"], []
        )
        assert result == ["ptp-must-gather"]

    def test_non_list_input(self):
        """Test that non-list input is returned as-is."""
        result = resolve_must_gather.resolve_must_gather(
            "not-a-list", SAMPLE_RELATED_IMAGES
        )
        assert result == "not-a-list"

    def test_non_list_related_images(self):
        """Test that non-list relatedImages returns input as-is."""
        result = resolve_must_gather.resolve_must_gather(
            ["ptp-must-gather"], "not-a-list"
        )
        assert result == ["ptp-must-gather"]

    def test_non_string_entry(self):
        """Test that non-string entries are kept as-is."""
        result = resolve_must_gather.resolve_must_gather(
            [42, None, "ptp-must-gather"], SAMPLE_RELATED_IMAGES
        )
        assert result == [
            42,
            None,
            "registry.redhat.io/openshift4/ptp-must-gather-rhel9@sha256:bbb222",
        ]

    def test_first_match_wins(self):
        """Test that the first matching relatedImage is used."""
        related = [
            {"name": "ptp-must-gather-rhel8", "image": "rhel8-image@sha256:111"},
            {"name": "ptp-must-gather-rhel9", "image": "rhel9-image@sha256:222"},
        ]
        result = resolve_must_gather.resolve_must_gather(
            ["ptp-must-gather"], related
        )
        # First match wins
        assert result == ["rhel8-image@sha256:111"]


class TestFilterModule:
    def test_filter_module_exposes_filter(self):
        """Test that FilterModule properly exposes the filter."""
        fm = resolve_must_gather.FilterModule()
        filters = fm.filters()
        assert "resolve_must_gather" in filters
        assert filters["resolve_must_gather"] == resolve_must_gather.resolve_must_gather

    def test_filter_module_callable(self):
        """Test that the filter can be called through FilterModule."""
        fm = resolve_must_gather.FilterModule()
        func = fm.filters()["resolve_must_gather"]
        result = func(["ose-must-gather"], SAMPLE_RELATED_IMAGES)
        assert result == [
            "registry.redhat.io/openshift4/ose-must-gather@sha256:aaa111"
        ]
