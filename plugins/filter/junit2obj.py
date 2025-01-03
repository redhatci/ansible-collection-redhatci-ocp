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

from __future__ import annotations
from typing import Any

__version__: str = "1.0.0"

DOCUMENTATION = r"""
  name: junit2obj
  version_added: "1.0.0"
  short_description: transform junit xml data as dictionary retaining suites and cases structure 
  description:
    - This filter plugin transforms a junit xml data to a dictionary for future conversion as JSON report
    - it is being implemented because `junit2dict` filter does not retain suites information (timings), hence not allowing collecting of running times as metrics for future analysis
  positional: xml_report_text
  options:
    - xml_report_text:
      description: The junit report xml text data
      type: str
      required: true
    - extra_metadata:
      description: additional metadata dict added at the root of resulting json object
      type: dict
      required: false
"""


EXAMPLES = r"""

    xml_data: |

    test_result: '{{ "path/to/junit.xml" | redhat.ocp.junit2obj }}'

    # =>
    #   {
    #
    #   }
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
    def filters(self) -> dict[str, Any]:
        return {
            "junit2obj": self.junit2obj,
        }

    def junit2obj(self, xml_report_text: str, extra_metadata: dict[str, Any] = {}) -> object:

        from junitparser import junitparser
        junit_xml: junitparser.JUnitXml = junitparser.JUnitXml.fromstring(xml_report_text)   # type: ignore

        report_dict: dict[str, Any]= {
            # "name": junit_xml.name, # type: ignore
            "time": junit_xml.time, # type: ignore
            "tests": junit_xml.tests, # type: ignore
            "failures": junit_xml.failures, # type: ignore
            "errors": junit_xml.errors, # type: ignore
            "skipped": junit_xml.skipped, # type: ignore
            "test_suites": []
        }
        if len(extra_metadata.keys()) > 0:
            report_dict.update(metadata=extra_metadata)
            report_dict["metadata"]["schema_version"] = __version__

        for suite in junit_xml: # type: ignore
            suite_dict: dict[str, Any] = {
                "name": suite.name, # type: ignore
                "time": suite.time, # type: ignore
                "tests": suite.tests, # type: ignore
                "failures": suite.failures, # type: ignore
                "errors": suite.errors, # type: ignore
                "skipped": suite.skipped, # type: ignore
                "test_cases": []
            }
            tstcase: junitparser.TestCase
            for tstcase in suite: # type: ignore
                case_dict: dict[str, Any] = {
                    "name": tstcase.name,            # type: ignore
                    "classname": tstcase.classname,  # type: ignore
                    "time": tstcase.time, # type: ignore
                    # "status":  None ,  # type: ignore
                    "result": None,     # Handle potential None result # type: ignore
                    "message": None,  # Handle potential None message # type: ignore
                    "type": None,           # Handle potential None type # type: ignore
                }
                for attr in ['result', 'type']:
                    if not hasattr(tstcase, attr): # type: ignore
                        continue
                    value = getattr(tstcase, attr)  # type: ignore
                    case_dict.update({attr: value}) # type: ignore
                    if attr != 'result':
                        continue
                    if hasattr(value, 'message'): # type: ignore
                        case_dict.update(message=value.message)
                suite_dict["test_cases"].append(case_dict)
            report_dict["test_suites"].append(suite_dict)
        return report_dict
