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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
__version__: str = "1.0.0"

import json
import time

try:
    from typing import Any  # for Python 3.8++
except ImportError:
    from typing_extensions import Any  # type: ignore  # for older Python versions
from typing import Dict  # type: ignore

from junitparser import junitparser as jup

DOCUMENTATION = r"""
  name: junit2obj
  version_added: "1.0.0"
  short_description: transform junit xml data as dictionary retaining suites and cases structure
  description: >
    This filter plugin transforms a junit xml data to a dictionary for future conversion as JSON report.
    It is being implemented because `junit2dict` filter does not retain suites information (timings),
    hence not allowing collecting of running times as metrics for future analysis.
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

    xml_report_text: |
        <?xml version="1.0" encoding="UTF-8"?>
        <testsuites tests="3" disabled="2" errors="0" failures="0" time="0.000426228">
            <testsuite name="Performance Addon Operator Reboot" package="/home/jenkins/workspace/CNF/cnf-compute-4.18"
                tests="3" disabled="0" skipped="2" errors="0" failures="0" time="0.000426228" timestamp="2024-12-12T20:12:23">
                <properties>
                    <property name="SuiteSucceeded" value="true"></property>
                    <property name="SuiteHasProgrammaticFocus" value="false"></property>
                    <property name="SpecialSuiteFailureReason" value=""></property>
                    <property name="SuiteLabels" value="[]"></property>
                    <property name="RandomSeed" value="1734025939"></property>
                    <property name="RandomizeAllSpecs" value="false"></property>
                    <property name="LabelFilter" value="(!openshift &amp;&amp; tier-0)"></property>
                </properties>
                <testcase name="[It] [disruptive][node][kubelet][devicemanager] Device management tests"
                    classname="Performance Addon Operator Reboot" status="skipped" time="0">
                    <skipped message="skipped"></skipped>
                </testcase>
                <testcase name="[It] [disruptive][node][kubelet][devicemanager] Device management tests [tier-3]"
                    classname="Performance Addon Operator Reboot" status="skipped" time="0">
                    <skipped message="skipped"></skipped>
                </testcase>
                <testcase name="[ReportAfterSuite] e2e serial suite"
                    classname="Performance Addon Operator Reboot" status="passed" time="6.826e-05">
                    <system-err>&gt; Enter [ReportAfterSuite] TOP-LEVEL - /home/jenkins/workspace/CNF/cnf-compute-4.18;</system-err>
                </testcase>
            </testsuite>
        </testsuites>


    test_result: '{{ "path/to/junit.xml" | redhat.ocp.junit2obj }}'
    # =>
    # {
    #     "time": 0.000426228,
    #     "tests": 3,
    #     "failures": 0,
    #     "errors": 0,
    #     "skipped": 2,
    #     "test_suites": [
    #         {
    #             "name": "Performance Addon Operator Reboot",
    #             "time": 0.0,
    #             "timestamp": "2024-12-12T20:12:23",
    #             "tests": 3,
    #             "failures": 0,
    #             "errors": 0,
    #             "skipped": 2,
    #             "properties": {
    #                 "SuiteSucceeded": "true",
    #                 "SuiteHasProgrammaticFocus": "false",
    #                 "SpecialSuiteFailureReason": "",
    #                 "SuiteLabels": "[]",
    #                 "RandomSeed": "1734025939",
    #                 "RandomizeAllSpecs": "false",
    #                 "LabelFilter": "(!openshift && tier-0)"
    #             },
    #             "test_cases": [
    #                 {
    #                     "name": "[It] [disruptive][node][kubelet][devicemanager] Device management tests",
    #                     "classname": "Performance Addon Operator Reboot",
    #                     "time": 0.0,
    #                     "result": [
    #                         {
    #                             "message": "skipped",
    #                             "status": "skipped"
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "name": "[It] [disruptive][node][kubelet][devicemanager] Device management tests [tier-3]",
    #                     "classname": "Performance Addon Operator Reboot",
    #                     "time": 0.0,
    #                     "result": [
    #                         {
    #                             "message": "skipped",
    #                             "status": "skipped"
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "name": "[ReportAfterSuite] e2e serial suite",
    #                     "classname": "Performance Addon Operator Reboot",
    #                     "time": 6.826e-05,
    #                     "result": [
    #                         {
    #                             "message": "passed",
    #                             "status": "passed"
    #                         }
    #                     ],
    #                     "system_err": "> &gt; Enter [ReportAfterSuite] TOP-LEVEL - /home/jenkins/workspace/CNF/cnf-compute-4.18;"
    #                 }
    #             ]
    #         }
    #     ]
    # }
"""


RETURN = r"""
  _value:
    description:
      - A list of dictionaries with testcase name and its status.
    type: any
"""


class FilterModule():
    """
    Filter converting junit XML report to a json string
    """

    def filters(self):
        """
        filter boilerplate
        """
        return {
            "junit2obj": self.junit2obj,
        }

    def _process_test_case(self, testcase: jup.TestCase):  # type: ignore
        """
        processing test case into a dict
        """
        curr_case: Dict[str, Any] = {}  # type: ignore
        curr_case.update({
            "name": str(testcase.name),  # type: ignore
            "classname": str(testcase.classname),  # type: ignore
        })
        case_time = testcase.time  # type: ignore
        if case_time is None:
            case_time = 0
        curr_case.update({"time": float(case_time)})  # type: ignore

        # Handle potential None results:
        attr = "result"
        curr_case.update({attr: None})

        if hasattr(testcase, attr):  # type: ignore
            attr_values: list[Any] = []  # type: ignore
            attr_dict: Dict[str, Any] = {}  # type: ignore
            value = getattr(testcase, attr)  # type: ignore
            for item in value:  # type: ignore
                attr_dict: Dict[str, Any] = {}  # type: ignore
                if item.message:
                    attr_dict["message"] = str(item.message)  # type: ignore
                if item.text:
                    attr_dict["text"] = str(item.text)  # type: ignore
                attr_dict["status"] = str(item.type)
                if item.type is None:  # type: ignore
                    attr_dict.update({"status": item.message.split(" ")[0]})  # type: ignore
                attr_values.append(attr_dict)
            if len(value) == 0:
                attr_dict.update({
                    "message": "passed",
                    "status": "passed",
                })
                attr_values.append(attr_dict)
            curr_case.update({attr: attr_values})

        for attr in ["system_err", "system_out"]:
            if not hasattr(testcase, attr):  # type: ignore
                continue
            value = getattr(testcase, attr)  # type: ignore
            if value is None:  # type: ignore
                continue
            curr_case[attr] = value

        return curr_case

    def _process_test_suite(self, testsuite: jup.TestSuite):  # type: ignore
        """
        processing test suite into a dict
        """
        curr_suite: Dict[str, Any] = {}         # type: ignore
        curr_suite.update({
            "name": str(testsuite.name),           # type: ignore
            "time": float(testsuite.time),         # type: ignore
        })
        if curr_suite.get("time") is None:      # type: ignore
            curr_suite.update({"time": float(0)})

        curr_suite.update({"timestamp": str(testsuite.timestamp)})  # type: ignore
        if curr_suite.get("timestamp") == "None":  # type: ignore
            curr_suite.update({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(0))})

        curr_suite.update({
            "tests": int(testsuite.tests),         # type: ignore
            "failures": int(testsuite.failures),   # type: ignore
            "errors": int(testsuite.errors),       # type: ignore
            "skipped": int(testsuite.skipped),     # type: ignore
        })
        if testsuite.properties is not None:  # type: ignore
            suite_properties: Dict[str, Any] = {}  # type: ignore
            for prop in testsuite.properties():  # type: ignore
                suite_properties.update({  # type: ignore
                    str(prop.name): prop.value,  # type: ignore
                })
            curr_suite.update({"properties": suite_properties})

        curr_suite.update({"test_cases": []})  # type: ignore
        tstcase: jup.TestCase  # type: ignore
        for tstcase in testsuite:  # type: ignore
            curr_case = self._process_test_case(tstcase)  # type: ignore
            curr_suite["test_cases"].append(curr_case)
        return curr_suite

    # pylint: disable=bad-whitespace
    def junit2obj(self, xml_report_text: str, extra_metadata: Dict[str, Any] | None = None) -> str:  # type: ignore
        """
        Convert junit XML Report into JSON.
        """
        junit_xml: jup.JUnitXml = jup.JUnitXml.fromstring(xml_report_text)  # type: ignore

        report: Dict[str, Any] = {}  # type: ignore

        report.update({
            "time": float(junit_xml.time),         # type: ignore
            "tests": int(junit_xml.tests),         # type: ignore
            "failures": int(junit_xml.failures),   # type: ignore
            "errors": int(junit_xml.errors),       # type: ignore
            "skipped": int(junit_xml.skipped),     # type: ignore
            "test_suites": [],                     # type: ignore
        })

        if extra_metadata is not None and len(extra_metadata.keys()) > 0:
            report.update({"metadata": extra_metadata})
            report["metadata"]["schema_version"] = __version__

        tstsuite: jup.TestSuite  # type: ignore
        for tstsuite in junit_xml:  # type: ignore
            curr_suite = self._process_test_suite(tstsuite)  # type: ignore
            report["test_suites"].append(curr_suite)

        result_text: str = json.dumps(dict(report), indent=4) + "\n"
        return result_text
