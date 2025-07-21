#!/usr/bin/env python
"""Ansible filter plugin that merges multiple json files into one

The files should be the result of junit2obj conversion
"""
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
from __future__ import annotations
from typing import Any
from ansible.utils.display import Display

__metaclass__ = type
__version__ = "1.0.0"

DOCUMENTATION = r"""
---
name: reportsmerger
version_added: "1.0.0"
short_description: merge multiple similarly built JSON files into one
description: >
  This filter plugin merges multiple test report JSON files (usually
  converted by junit2obj filter) into a single consolidated test report.
  It combines all test suites and recalculates aggregated statistics.
positional: filenames
options:
  filenames:
    description: List of filenames containing test report JSON data
    type: list
    elements: str
    required: true
"""

EXAMPLES = r"""
---
# Merge multiple test report files
- name: merge reports
  ansible.builtin.set_fact:
    merged: "{{ ['1.json', '2.json', '3.json'] | redhatci.ocp.reportsmerger }}"

# The result will be a merged test report with:
# - Combined test_suites list from all input files
# - Aggregated statistics (tests, failures, errors, skipped counts, total time)
"""

RETURN = r"""
---
_value:
  description:
    - Merged test report data structure
  type: dict
  contains:
    time:
      description: Total time from all test suites
      type: float
    tests:
      description: Total number of tests
      type: int
    failures:
      description: Total number of failures
      type: int
    errors:
      description: Total number of errors
      type: int
    skipped:
      description: Total number of skipped tests
      type: int
    test_suites:
      description: Combined list of all test suites from input files
      type: list
    schema_version:
      description: Schema version
      type: str
"""


class FilterModule:
    """
    Filter for merging multiple test report JSON files
    """

    def filters(self) -> dict[str, Any]:
        """
        filter boilerplate
        """
        return {
            "reportsmerger": self.reportsmerger,
        }

    def reportsmerger(
        self, filenames: list[str], output_file: str|None = None
    ) -> dict[str, Any]|str:
        """
        Merge multiple test report JSON files into a single test report.

        Args:
            filenames: List of file paths containing test report JSON data
            output_file: Optional output file path. If provided, writes merged
                         data to file and returns the file path instead of
                         the data

        Returns:
            dict: Merged report with aggregated statistics (if no output_file)
            str: Output file path (if output_file provided)
        """
        import json
        import os

        display = Display()
        if not isinstance(filenames, list):
            raise TypeError("reportsmerger expects a list of filenames")
        if not filenames:
            raise ValueError("reportsmerger requires at least one filename")

        merged_report: dict[str, Any] = {
            "time": 0.0,
            "tests": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "test_suites": [],
            "schema_version": __version__,
        }

        for filename in filenames:
            if not os.path.exists(filename):
                msg = (
                    f"reportsmerger plugin: file {filename} "
                    "does not exist and was skipped"
                )
                display.warning(msg)
                continue

            report_data = self._load_and_validate_report(filename, display)
            self._accumulate_report_stats(report_data, merged_report, filename, display)
        msg: str = "\n".join(
            [
                f"Merged {len(filenames)} files:",
                f"  tests:\t{merged_report['tests']}",
                f"  failures:\t{merged_report['failures']}",
                f"  errors:\t{merged_report['errors']}",
                f"  skipped:\t{merged_report['skipped']}",
                f"  time:\t{merged_report['time']}",
                f"  test_suites:\t{len(merged_report['test_suites'])}",
            ]
        )
        display.v(msg)

        # NEW: If output file specified, write directly and return path
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(merged_report, f, indent=2)
            display.v(f"Merged report written to {output_file}")
            return output_file  # Return just the path, not the data

        # Original behavior: return the data
        return merged_report

    def _load_and_validate_report(
        self, filename: str, display: Display
    ) -> dict[str, Any]:
        """Load and validate a single report file."""
        import json

        try:
            with open(filename, "r", encoding="utf-8") as f:
                report_data: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as jde:
            msg = f"Invalid JSON in file {filename}: {jde}"
            display.error(msg)
            raise ValueError(msg) from jde
        except Exception as exc:
            msg = f"Error reading file {filename}: {exc}"
            display.error(msg)
            raise RuntimeError(msg) from exc

        # Validate required fields
        if "test_suites" not in report_data:
            msg = f"Missing 'test_suites' field in {filename}"
            display.error(msg)
            raise ValueError(msg)

        return report_data

    def _accumulate_report_stats(
        self,
        report_data: dict[str, Any],
        merged_report: dict[str, Any],
        filename: str,
        display: Display,
    ) -> None:
        """Accumulate statistics from a report into the merged report."""
        # Update numeric statistics directly in merged_report
        for field in ["time", "tests", "failures", "errors", "skipped"]:
            value = report_data.get(field, 0)
            if value is not None:
                try:
                    if field == "time":
                        merged_report[field] += float(value)
                    else:
                        merged_report[field] += int(value)
                except (ValueError, TypeError) as e:
                    msg = f"Invalid numeric data in {filename}: {e}"
                    display.error(msg)
                    raise ValueError(msg) from e

        # Merge test suites
        test_suites = report_data.get("test_suites", [])
        if not isinstance(test_suites, list):
            msg = f"Invalid 'test_suites' format in {filename}: expected list"
            display.error(msg)
            raise ValueError(msg)

        merged_report["test_suites"].extend(test_suites)
        msg = f"Successfully processed {filename}: {report_data.get('tests', 0)} tests"
        display.vv(msg)
