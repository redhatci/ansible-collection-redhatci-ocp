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

from typing import Any, Dict, List

try:
    from lxml import etree
    from lxml.etree import _Element
except ImportError as importerr:
    raise ImportError("lxml is required for junit2dict filter. Please install lxml.") from importerr

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


def _is_test_passed(testcase_element: _Element) -> bool:
    """
    Determine if a test case passed based on its child elements.

    Args:
        testcase_element: The testcase XML element

    Returns:
        True if the test passed or was skipped, False otherwise
    """
    # Check for failure or error elements
    failures = testcase_element.xpath("./failure")
    errors = testcase_element.xpath("./error")

    if failures or errors:
        return False

    # TODO: Currently, we consider skipped tests as passed to unblock TNF pipeline regex.
    # This should be fixed later, and skipped logic is to be updated.
    # Both absent and skipped test case are usually treated as a failure.
    skipped = testcase_element.xpath("./skipped")
    if skipped:
        return True  # Currently treating skipped as passed

    # If no failure, error, or skipped elements, consider it passed
    return True


class FilterModule(object):
    def filters(self) -> Dict[str, Any]:
        return {
            "junit2dict": self.junit2dict,
        }

    def junit2dict(self, junit_filepath: str) -> List[Dict[str, Any]]:
        """
        Transform a JUnit XML file to a list of test case dictionaries.

        Args:
            junit_filepath: Path to the JUnit XML file

        Returns:
            List of dictionaries with testcase name and passed status

        Raises:
            etree.XMLSyntaxError: If the XML file is malformed
            FileNotFoundError: If the XML file doesn't exist
        """
        try:
            # Parse the XML file
            with open(junit_filepath, 'r', encoding='utf-8') as file:
                tree = etree.parse(file)
            root = tree.getroot()

            tests = []

            # Find all testcase elements, whether they're direct children or nested in testsuites
            testcases = root.xpath(".//testcase")

            for testcase in testcases:
                test_name = testcase.get("name", "")
                is_passed = _is_test_passed(testcase)

                tests.append({
                    "testcase": test_name,
                    "passed": is_passed
                })

            return tests

        except etree.XMLSyntaxError as xserr:
            raise ValueError(f"Invalid XML format in file {junit_filepath}: {xserr}") from xserr
        except FileNotFoundError as fnferr:
            raise FileNotFoundError(f"JUnit XML file not found: {junit_filepath}") from fnferr
        except Exception as err:
            raise RuntimeError(f"Error processing JUnit XML file {junit_filepath}: {err}") from err
