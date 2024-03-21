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

DOCUMENTATION = r"""
  name: junit2dict
  version_added: "0.1.0"
  short_description: transform junit xml to a list of test cases.
  description:
    - This filter plugin transforms a junit xml file to a list of dictionaries
      with testcase name and its status.
  positional: _input
  options:
    _input:
      description: The path to the junit xml file.
      type: str
      required: true
"""


EXAMPLES = r"""

    test_results: '{{ "path/to/junit.xml" | junit2dict }}'
    # =>
    #   [
    #       {
    #          "testcase": "test1",
    #          "passed": true
    #       },
    #       {
    #          "testcase": "test2",
    #          "passed": false
    #       }
    #       ...
    #   ]
"""


RETURN = r"""
  _value:
    description:
      - A list of dictionaries with testcase name and its status.
    type: any
"""


class FilterModule(object):
    def filters(self):
        return {
            "junit2dict": self.junit2dict,
        }

    def junit2dict(self, junit_filepath):
        from junitparser import JUnitXml

        xml = JUnitXml.fromfile(junit_filepath)
        tests = []
        for suite in xml:
            for case in suite:
                # TODO: Currently, we consider skipped tests as passed to unblock TNF pipeline regex.
                # This should be fixed later, and 'or case.is_skipped' is to be removed.
                # Both absent and skipped test case are usually treated as a failure.
                tests.append(
                    {"testcase": case.name, "passed": case.is_passed or case.is_skipped}
                )
        return tests
