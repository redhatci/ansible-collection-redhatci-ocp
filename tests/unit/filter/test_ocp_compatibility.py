#
# Copyright (C) 2024 Red Hat, Inc.
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

import os
import tempfile
import json
import unittest

from ansible_collections.redhatci.ocp.plugins.filter import ocp_compatibility


class TestOcpCompatibility(unittest.TestCase):
    def test_filter_with_no_deprecated_api_with_empty_array(self):
        filter = ocp_compatibility.FilterModule()

        with tempfile.TemporaryDirectory() as tmpdirname:
            self.assertEqual(
                filter.filters()["ocp_compatibility"](
                    [], "4.15", os.path.join(tmpdirname, "junit.xml")
                ),
                {"4.15": "compatible", "4.16": "compatible"},
            )

    def test_filter_with_deprecated_api_in_non_empty_list(self):
        filter = ocp_compatibility.FilterModule()
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_ocp_compatibility_data.json')

        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        with tempfile.TemporaryDirectory() as tmpdirname:
            actual_result = filter.filters()["ocp_compatibility"](
                json_data, "4.13", os.path.join(tmpdirname, "junit.xml"))

            # The order of elements in a dictionary is not guaranteed in Python.
            # Have to sort before comparing to avoid random failures.
            actual_result["4.16"] = ", ".join(sorted(actual_result["4.16"].split(", ")))

            expected_result = {
                "4.13": "compatible",
                "4.14": "compatible",
                "4.15": "compatible",
                "4.16": "flowschemas.v1beta2.flowcontrol.apiserver.k8s.io, prioritylevelconfigurations.v1beta2.flowcontrol.apiserver.k8s.io",
            }

            self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()

# test_ocp_compatibility.py ends here
