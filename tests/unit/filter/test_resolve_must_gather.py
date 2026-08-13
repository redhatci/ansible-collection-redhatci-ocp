#
# Copyright (C) 2026 Red Hat, Inc.
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


class TestResolveMustGather:
    def test_exact_hyphen_match_returns_sha256_pinned_ref(self):
        """Exact hyphen name matches a digest-pinned image reference."""
        image_list = [
            "registry.redhat.io/openshift4/ose-must-gather@sha256:abc123",
            "registry.redhat.io/openshift4/ose-network-tools@sha256:def456",
        ]
        result = resolve_must_gather.resolve_must_gather("ose-must-gather", image_list)
        assert result == "registry.redhat.io/openshift4/ose-must-gather@sha256:abc123"

    def test_underscore_vs_hyphen_normalisation_matches(self):
        """Underscore in short_name matches a hyphenated image segment."""
        image_list = [
            "registry.redhat.io/openshift4/ose-network-tools@sha256:def456",
            "registry.redhat.io/openshift4/ose-must-gather@sha256:abc123",
        ]
        result = resolve_must_gather.resolve_must_gather("ose_must_gather", image_list)
        assert result == "registry.redhat.io/openshift4/ose-must-gather@sha256:abc123"

    def test_no_match_returns_empty_string(self):
        """Returns empty string when no image matches the short name."""
        image_list = [
            "registry.redhat.io/openshift4/ose-network-tools@sha256:def456",
            "registry.redhat.io/openshift4/ose-cli@sha256:ghi789",
        ]
        result = resolve_must_gather.resolve_must_gather("ose-must-gather", image_list)
        assert result == ""

    def test_filter_module_exposes_resolve_must_gather_callable(self):
        """FilterModule.filters() exposes 'resolve_must_gather' as a callable."""
        filter_module = resolve_must_gather.FilterModule()
        filters = filter_module.filters()
        assert "resolve_must_gather" in filters
        assert callable(filters["resolve_must_gather"])
