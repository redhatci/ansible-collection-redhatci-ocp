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

import json
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../plugins/filter"))
import json2junit


class TestJson2Junit(unittest.TestCase):
    def test_filter_converts_top_level_rule_list(self):
        filter_module = json2junit.FilterModule()
        input_path = os.path.join(
            os.path.dirname(__file__), "../data/test_json2junit_sample_input.json"
        )

        with open(input_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        with tempfile.TemporaryDirectory() as tmpdirname:
            junit_path = os.path.join(tmpdirname, "checks-junit.xml")
            result = filter_module.filters()["json2junit"](json_data, junit_path, "In-cluster checks")

            self.assertEqual(result, junit_path)
            root = ET.parse(junit_path).getroot()
            test_cases = root.findall(".//testcase")
            self.assertEqual(len(test_cases), 4)
            self.assertEqual(root.get("failures"), "2")
            self.assertEqual(root.get("tests"), "4")

            skipped = root.findall(".//skipped")
            self.assertEqual(len(skipped), 1)

            clock_sync_failure = root.find(".//testcase[@name='linux|clock_synchronized']/failure")
            self.assertIsNotNone(clock_sync_failure)
            self.assertIn("NTP wrong values", clock_sync_failure.get("message", ""))


if __name__ == "__main__":
    unittest.main()
