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

DOCUMENTATION = r"""
  name: json2junit
  version_added: "1.0.0"
  short_description: Convert JSON health-check results to JUnit XML.
  description:
    - Converts JSON rule/check results into a JUnit XML report file.
    - Accepts a top-level list of rule reports or nested JSON structures
      containing rule objects with rule_id/key and status fields.
  positional: _input
  options:
    _input:
      description: JSON data structure or list of rule reports.
      type: raw
      required: true
    junit_output_file:
      description: Destination path for the generated JUnit XML file.
      type: str
      required: true
    suite_name:
      description: Name of the JUnit testsuite element.
      type: str
      default: JSON checks
"""

_FAIL_STATUSES = frozenset({"fail", "failed"})
_WARNING_STATUSES = frozenset({"warning"})
_SKIP_STATUSES = frozenset({"skip", "na", "not_applicable"})
_PASS_STATUSES = frozenset({"pass", "passed", "info"})
_MESSAGE_STATUSES = _FAIL_STATUSES | _WARNING_STATUSES | _SKIP_STATUSES
_MAX_MESSAGE_LENGTH = 4000


class FilterModule:
    def filters(self):
        return {
            "json2junit": self.json2junit,
        }

    def json2junit(self, json_data, junit_output_file, suite_name="JSON checks"):
        from junit_xml import TestCase, TestSuite, to_xml_report_file

        reports = self._extract_reports(json_data)
        test_cases = []

        for report in reports:
            name = report.get("rule_id") or report.get("key") or report.get("description") or "unknown"
            classname = report.get("domain") or report.get("component") or "json_checks"
            status = (report.get("status") or "").lower()
            test_case = TestCase(name, classname=classname)

            if status in _FAIL_STATUSES:
                test_case.add_failure_info(self._build_message(report))
            elif status in _WARNING_STATUSES:
                test_case.add_failure_info(self._build_message(report) or "warning")
            elif status in _SKIP_STATUSES:
                test_case.add_skipped_info(self._build_message(report) or status)
            elif status not in _PASS_STATUSES and status:
                test_case.add_failure_info(self._build_message(report) or status)

            test_cases.append(test_case)

        test_suite = TestSuite(suite_name, test_cases)

        with open(junit_output_file, "w", encoding="utf-8") as junit_file:
            to_xml_report_file(junit_file, [test_suite])

        return junit_output_file

    def _is_report(self, obj):
        return (
            isinstance(obj, dict)
            and "status" in obj
            and ("rule_id" in obj or "key" in obj)
        )

    def _extract_reports(self, json_data):
        reports = []

        def walk(node):
            if isinstance(node, list):
                for item in node:
                    if self._is_report(item):
                        reports.append(item)
                    else:
                        walk(item)
            elif isinstance(node, dict):
                if self._is_report(node):
                    reports.append(node)
                else:
                    for value in node.values():
                        walk(value)

        walk(json_data)
        return reports

    def _build_message(self, report):
        details = report.get("details") or []
        messages = []

        for detail in details:
            if not isinstance(detail, dict):
                continue

            detail_status = (detail.get("status") or "").lower()
            if detail_status not in _MESSAGE_STATUSES:
                continue

            host = detail.get("node_name") or detail.get("node_ip") or "unknown"
            message = (
                detail.get("message")
                or detail.get("describe_msg")
                or detail.get("exception")
                or detail_status
            )
            messages.append(f"{host}: {self._truncate(message)}")

        if messages:
            return "; ".join(messages)

        fallback = report.get("description") or report.get("status") or ""
        return self._truncate(fallback)

    def _truncate(self, message):
        message = str(message)
        if len(message) <= _MAX_MESSAGE_LENGTH:
            return message
        return message[:_MAX_MESSAGE_LENGTH] + "..."
