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


PTP_CSV = {
    "name": "ptp-operator.v4.18.0",
    "display_name": "PTP Operator",
    "annotations": {
        "operators.openshift.io/must-gather-image": (
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ),
    },
    "related_images": [
        {
            "name": "ptp-operator",
            "image": "registry.redhat.io/openshift5/ptp-operator@sha256:op",
        },
        {
            "name": "ptp-must-gather-rhel9",
            "image": "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptprel",
        },
    ],
}

ACM_CSV = {
    "name": "advanced-cluster-management.v2.12.0",
    "display_name": "Advanced Cluster Management for Kubernetes",
    "annotations": {
        "operators.openshift.io/must-gather-image": (
            "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:acmann"
        ),
    },
    "related_images": [
        {
            "name": "acm-operator",
            "image": "registry.redhat.io/rhacm2/acm-operator@sha256:op",
        },
    ],
}

GITOPS_RELATED_ONLY = {
    "name": "openshift-gitops-operator.v1.16.0",
    "display_name": "OpenShift GitOps",
    "annotations": {},
    "related_images": [
        {
            "name": "must_gather_image",
            "image": (
                "registry.redhat.io/openshift-gitops-1/"
                "must-gather-rhel9@sha256:gitopsrel"
            ),
        },
        {
            "name": "gitops-operator",
            "image": (
                "registry.redhat.io/openshift-gitops-1/"
                "gitops-rhel9-operator@sha256:op"
            ),
        },
    ],
}

MESH_OTHER_ANN = {
    "name": "servicemeshoperator.v2.6.0",
    "display_name": "OpenShift Service Mesh",
    "annotations": {
        "images.v1_28_8.must-gather": (
            "registry.redhat.io/openshift-service-mesh/"
            "istio-must-gather-rhel9@sha256:meshann"
        ),
    },
    "related_images": [],
}

SAMPLE_CSVS = [PTP_CSV, ACM_CSV, GITOPS_RELATED_ONLY]


class TestResolveMustGather:
    def test_annotation_preferred_over_related_images(self):
        result = resolve_must_gather.resolve_must_gather(["ptp"], SAMPLE_CSVS)
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]

    def test_keyword_identifies_csv_without_hint_in_csv_name(self):
        """'acm' is not in the CSV name; annotation image path identifies it."""
        result = resolve_must_gather.resolve_must_gather(["acm"], SAMPLE_CSVS)
        assert result == [
            "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:acmann"
        ]

    def test_related_images_used_when_annotation_missing(self):
        result = resolve_must_gather.resolve_must_gather(
            ["gitops"], SAMPLE_CSVS
        )
        assert result == [
            "registry.redhat.io/openshift-gitops-1/must-gather-rhel9@sha256:gitopsrel"
        ]

    def test_other_must_gather_annotation(self):
        result = resolve_must_gather.resolve_must_gather(
            ["servicemesh"], [MESH_OTHER_ANN]
        )
        assert result == [
            "registry.redhat.io/openshift-service-mesh/"
            "istio-must-gather-rhel9@sha256:meshann"
        ]

    def test_full_reference_ignored(self):
        full_ref = "registry.redhat.io/openshift4/custom-image:v4.18"
        result = resolve_must_gather.resolve_must_gather(
            [full_ref], SAMPLE_CSVS
        )
        assert result == []

    def test_mixed_hints_ignore_full_reference(self):
        result = resolve_must_gather.resolve_must_gather(
            [
                "ptp",
                "registry.redhat.io/openshift4/custom-image:latest",
                "acm",
            ],
            SAMPLE_CSVS,
        )
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann",
            "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:acmann",
        ]

    def test_unresolved_hint_omitted(self):
        result = resolve_must_gather.resolve_must_gather(
            ["nonexistent", "ptp"], SAMPLE_CSVS
        )
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]

    def test_no_fallback_registry(self):
        result = resolve_must_gather.resolve_must_gather(
            ["ose-must-gather"], SAMPLE_CSVS
        )
        assert result == []

    def test_empty_image_list(self):
        result = resolve_must_gather.resolve_must_gather([], SAMPLE_CSVS)
        assert result == []

    def test_empty_csvs(self):
        result = resolve_must_gather.resolve_must_gather(["ptp"], [])
        assert result == []

    def test_non_list_input(self):
        result = resolve_must_gather.resolve_must_gather(
            "not-a-list", SAMPLE_CSVS
        )
        assert result == "not-a-list"

    def test_non_list_csvs(self):
        result = resolve_must_gather.resolve_must_gather(
            ["ptp"], "not-a-list"
        )
        assert result == []

    def test_non_string_entry_omitted(self):
        result = resolve_must_gather.resolve_must_gather(
            [42, None, "ptp"], SAMPLE_CSVS
        )
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]

    def test_null_csv_fields_from_json_query(self):
        """json_query sets missing CSV fields to None, not omitted keys."""
        csvs = [
            {
                "name": "ptp-operator.v4.18.0",
                "display_name": None,
                "annotations": {
                    "operators.openshift.io/must-gather-image": (
                        "registry.redhat.io/openshift5/"
                        "ptp-must-gather-rhel9@sha256:ptpann"
                    ),
                },
                "related_images": [
                    {
                        "name": None,
                        "image": (
                            "registry.redhat.io/openshift5/"
                            "ptp-must-gather-rhel9@sha256:ptprel"
                        ),
                    },
                ],
            }
        ]
        result = resolve_must_gather.resolve_must_gather(["ptp"], csvs)
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]

    def test_prefers_annotated_csv_when_multiple_match(self):
        related_only_ptp = {
            "name": "other-ptp.v1.0.0",
            "display_name": "Other PTP",
            "annotations": {},
            "related_images": [
                {
                    "name": "ptp-must-gather-rhel8",
                    "image": "registry.example/ptp-must-gather-rhel8@sha256:old",
                },
            ],
        }
        result = resolve_must_gather.resolve_must_gather(
            ["ptp"], [related_only_ptp, PTP_CSV]
        )
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]

    def test_legacy_flat_related_images(self):
        related = [
            {
                "name": "acm_must_gather",
                "image": "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:aaa",
            },
            {
                "name": "acm-operator",
                "image": "registry.redhat.io/rhacm2/acm-operator@sha256:bbb",
            },
        ]
        result = resolve_must_gather.resolve_must_gather(["acm"], related)
        assert result == [
            "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:aaa"
        ]

    def test_keyword_skips_non_must_gather_related_image(self):
        csvs = [
            {
                "name": "openshift-gitops-operator.v1.16.0",
                "display_name": "OpenShift GitOps",
                "annotations": {},
                "related_images": [
                    {
                        "name": "gitops-operator",
                        "image": (
                            "registry.redhat.io/openshift-gitops-1/"
                            "gitops-rhel9-operator@sha256:bbb"
                        ),
                    },
                ],
            }
        ]
        result = resolve_must_gather.resolve_must_gather(["gitops"], csvs)
        assert result == []

    def test_mustgather_without_hyphen(self):
        """OADP ships oadp-mustgather (no hyphen) in relatedImages."""
        csvs = [
            {
                "name": "oadp-operator.v1.6.1",
                "display_name": "OADP Operator",
                "annotations": {},
                "related_images": [
                    {
                        "name": "oadp-mustgather-rhel9",
                        "image": (
                            "registry.redhat.io/oadp/"
                            "oadp-mustgather-rhel9@sha256:oadp"
                        ),
                    },
                    {
                        "name": "oadp-rhel9-operator",
                        "image": (
                            "registry.redhat.io/oadp/"
                            "oadp-rhel9-operator@sha256:op"
                        ),
                    },
                ],
            }
        ]
        result = resolve_must_gather.resolve_must_gather(["oadp"], csvs)
        assert result == [
            "registry.redhat.io/oadp/oadp-mustgather-rhel9@sha256:oadp"
        ]

    def test_duplicate_resolved_images_unique(self):
        result = resolve_must_gather.resolve_must_gather(
            ["ptp", "ptp-must-gather", "acm", "acm"], SAMPLE_CSVS
        )
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann",
            "registry.redhat.io/rhacm2/acm-must-gather-rhel9@sha256:acmann",
        ]

    def test_different_hints_same_image_unique(self):
        csvs = [
            {
                "name": "multicluster-engine.v5.0.0",
                "display_name": "Multicluster Engine",
                "annotations": {
                    "operators.openshift.io/must-gather-image": (
                        "registry.redhat.io/multicluster-engine/"
                        "must-gather-rhel9@sha256:mce"
                    ),
                },
                "related_images": [],
            }
        ]
        result = resolve_must_gather.resolve_must_gather(
            ["mce", "multicluster-engine"], csvs
        )
        assert result == [
            "registry.redhat.io/multicluster-engine/must-gather-rhel9@sha256:mce"
        ]


class TestFilterModule:
    def test_filter_module_exposes_filter(self):
        fm = resolve_must_gather.FilterModule()
        filters = fm.filters()
        assert "resolve_must_gather" in filters
        assert (
            filters["resolve_must_gather"]
            == resolve_must_gather.resolve_must_gather
        )

    def test_filter_module_callable(self):
        fm = resolve_must_gather.FilterModule()
        func = fm.filters()["resolve_must_gather"]
        result = func(["ptp"], SAMPLE_CSVS)
        assert result == [
            "registry.redhat.io/openshift5/ptp-must-gather-rhel9@sha256:ptpann"
        ]
