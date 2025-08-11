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

# pylint: disable=invalid-name
__metaclass__ = type
__version__ = "1.1.0"

DOCUMENTATION = r"""
---
name: reportsmerger
version_added: "1.1.0"
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
  output_file:
    description: Optional output file path to write merged data
    type: str
    required: false
  strategy:
    description: Optimization strategy for merging performance
    type: str
    required: false
    default: normal
    choices:
      - normal
      - large
      - many
      - shallow
      - complex
"""

EXAMPLES = r"""
---
# Basic usage - merge multiple test report files
- name: merge reports (default strategy)
  ansible.builtin.set_fact:
    merged: "{{ ['1.json', '2.json', '3.json'] | redhatci.ocp.reportsmerger }}"

# Use optimization strategies for different scenarios
- name: merge large files with memory optimization
  ansible.builtin.set_fact:
    merged: "{{ large_files | redhatci.ocp.reportsmerger(strategy='large') }}"

- name: merge many files with parallel processing
  ansible.builtin.set_fact:
    merged: "{{ many_files | redhatci.ocp.reportsmerger(strategy='many') }}"

- name: get stats only with lazy test suites loading
  ansible.builtin.set_fact:
    stats: "{{ files | redhatci.ocp.reportsmerger(strategy='shallow') }}"

- name: merge complex files skipping heavy test case details
  ansible.builtin.set_fact:
    lightweight: "{{ complex_files | redhatci.ocp.reportsmerger(strategy='complex') }}"

# Write output directly to file
- name: merge and save to file
  ansible.builtin.set_fact:
    output_path: "{{ files | redhatci.ocp.reportsmerger(output_file='/tmp/merged.json') }}"
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

    # pylint: disable=bad-whitespace
    def reportsmerger(
        self,
        filenames: list[str],
        strategy: str = "normal",
        output_file: str | None = None,
    ) -> dict[str, Any] | str:
        """
        Merge multiple test report JSON files into a single test report.

        Args:
            filenames: List of file paths containing test report JSON data
            strategy: Optimization strategy to use:
                     - "normal": Default behavior (backward compatible)
                     - "large": Streaming aggregation for large files (low memory)
                     - "many": Parallel processing for many files (faster I/O)
                     - "shallow": Lazy test suites loading (stats-only focus)
                     - "complex": Schema-specific parsing (skip heavy test_cases)
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

        strategy_chooser = {
            "normal": self._strategy_normal,
            "large": self._strategy_large_streaming,
            "many": self._strategy_many_parallel,
            "shallow": self._strategy_shallow_lazy,
            "complex": self._strategy_complex_parsing,
        }
        # Validate output_file parameter
        if output_file and not isinstance(output_file, str):
            raise ValueError("output_file must be a string")
        # Validate strategy parameter
        if strategy not in strategy_chooser:
            raise ValueError(f"Invalid strategy '{strategy}'. Must be one of: {list(strategy_chooser.keys())}")

        # Strategy dispatch
        strategy_handler = strategy_chooser[strategy]
        merged_report = strategy_handler(filenames, display)

        msg: str = "\n".join(
            [
                f"Merged {len(filenames)} files using '{strategy}' strategy:",
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

    def _strategy_normal(self, filenames: list[str], display: Display) -> dict[str, Any]:
        """Normal strategy - current behavior (backward compatible)"""
        import os

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

        return merged_report

    def _strategy_large_streaming(self, filenames: list[str], display: Display) -> dict[str, Any]:
        """Large files strategy - streaming aggregation for memory efficiency"""
        import json
        import os

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
                msg = f"reportsmerger plugin: file {filename} does not exist and was skipped"
                display.warning(msg)
                continue

            try:
                # Stream processing - load, accumulate, discard immediately
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Validate required fields
                if "test_suites" not in data:
                    raise ValueError(f"Missing 'test_suites' field in {filename}")

                # Direct accumulation without intermediate storage
                merged_report["time"] += float(data.get("time", 0.0))
                merged_report["tests"] += int(data.get("tests", 0))
                merged_report["failures"] += int(data.get("failures", 0))
                merged_report["errors"] += int(data.get("errors", 0))
                merged_report["skipped"] += int(data.get("skipped", 0))

                # Efficient list extension
                test_suites = data.get("test_suites", [])
                merged_report["test_suites"].extend(test_suites)

                display.vv(f"Streamed {filename}: {data.get('tests', 0)} tests")

                # Explicit cleanup for memory efficiency
                del data, test_suites

            except Exception as e:
                msg = f"Error processing {filename}: {e}"
                display.error(msg)
                raise ValueError(msg) from e

        return merged_report

    def _strategy_many_parallel(self, filenames: list[str], display: Display) -> dict[str, Any]:
        """Many files strategy - parallel processing for I/O efficiency"""
        import json
        import os
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # Thread-safe accumulator
        stats_lock = threading.Lock()
        merged_stats = {"time": 0.0, "tests": 0, "failures": 0, "errors": 0, "skipped": 0}
        all_test_suites = []
        processing_errors = []

        def process_single_file(filename: str) -> tuple[dict, list, str | None]:
            """Process a single file and return stats, suites, and any error"""
            if not os.path.exists(filename):
                return {}, [], f"File {filename} does not exist"

            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if "test_suites" not in data:
                    return {}, [], f"Missing 'test_suites' field in {filename}"

                local_stats = {
                    "time": float(data.get("time", 0.0)),
                    "tests": int(data.get("tests", 0)),
                    "failures": int(data.get("failures", 0)),
                    "errors": int(data.get("errors", 0)),
                    "skipped": int(data.get("skipped", 0))
                }
                local_suites = data.get("test_suites", [])

                return local_stats, local_suites, None

            except Exception as e:
                return {}, [], f"Error processing {filename}: {e}"

        # Process files in parallel (max 4 threads for I/O bound work)
        with ThreadPoolExecutor(max_workers=min(4, len(filenames))) as executor:
            future_to_filename = {executor.submit(process_single_file, f): f for f in filenames}

            for future in as_completed(future_to_filename):
                filename = future_to_filename[future]
                local_stats, local_suites, error = future.result()

                if error:
                    if "does not exist" in error:
                        display.warning(f"reportsmerger plugin: {error} and was skipped")
                    else:
                        processing_errors.append(error)
                    continue

                # Thread-safe accumulation
                with stats_lock:
                    for key in merged_stats:
                        merged_stats[key] += local_stats[key]
                    all_test_suites.extend(local_suites)

                display.vv(f"Processed {filename}: {local_stats['tests']} tests")

        # Handle any processing errors
        if processing_errors:
            error_msg = "; ".join(processing_errors)
            display.error(error_msg)
            raise ValueError(error_msg)

        return {
            **merged_stats,
            "test_suites": all_test_suites,
            "schema_version": __version__,
        }

    def _strategy_shallow_lazy(self, filenames: list[str], display: Display) -> dict[str, Any]:
        """Shallow strategy - lazy test suites loading for stats-focused operations"""
        import json
        import os

        class LazyTestSuites:
            """Lazy-loaded test suites that only merge when accessed"""
            def __init__(self, file_list: list[str], display_obj: Display):
                self._files = file_list
                self._display = display_obj
                self._merged_suites = None
                self._length = None

            def __iter__(self):
                if self._merged_suites is None:
                    self._load_all_suites()
                # _merged_suites is guaranteed to be a list after _load_all_suites()
                return iter(self._merged_suites or [])

            def __len__(self):
                if self._length is None:
                    self._calculate_length()
                return self._length

            def _calculate_length(self):
                """Calculate total number of test suites without loading them"""
                total = 0
                for filename in self._files:
                    if not os.path.exists(filename):
                        continue
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total += len(data.get("test_suites", []))
                    except Exception:
                        continue
                self._length = total

            def _load_all_suites(self):
                """Load all test suites when actually needed"""
                self._merged_suites = []
                for filename in self._files:
                    if not os.path.exists(filename):
                        continue
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            self._merged_suites.extend(data.get("test_suites", []))
                    except Exception as e:
                        self._display.warning(f"Error loading suites from {filename}: {e}")

        # Fast stats-only accumulation
        merged_stats = {"time": 0.0, "tests": 0, "failures": 0, "errors": 0, "skipped": 0}

        for filename in filenames:
            if not os.path.exists(filename):
                msg = f"reportsmerger plugin: file {filename} does not exist and was skipped"
                display.warning(msg)
                continue

            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if "test_suites" not in data:
                    raise ValueError(f"Missing 'test_suites' field in {filename}")

                # Only accumulate top-level stats
                merged_stats["time"] += float(data.get("time", 0.0))
                merged_stats["tests"] += int(data.get("tests", 0))
                merged_stats["failures"] += int(data.get("failures", 0))
                merged_stats["errors"] += int(data.get("errors", 0))
                merged_stats["skipped"] += int(data.get("skipped", 0))

                display.vv(f"Stats from {filename}: {data.get('tests', 0)} tests")

            except Exception as e:
                msg = f"Error processing {filename}: {e}"
                display.error(msg)
                raise ValueError(msg) from e

        return {
            **merged_stats,
            "test_suites": LazyTestSuites(filenames, display),
            "schema_version": __version__,
        }

    def _strategy_complex_parsing(self, filenames: list[str], display: Display) -> dict[str, Any]:
        """Complex strategy - schema-specific parsing to skip heavy test_cases"""
        import json
        import os

        class TestSuiteOnlyDecoder(json.JSONDecoder):
            """Custom decoder that strips heavy test_cases data during parsing"""
            def decode(self, s):
                obj = super().decode(s)
                # Keep suite metadata but remove heavy test_cases details
                if "test_suites" in obj:
                    for suite in obj["test_suites"]:
                        if "test_cases" in suite:
                            # Keep count but remove detailed test case data
                            test_cases_count = len(suite["test_cases"])
                            suite["test_cases"] = []
                            # Preserve the fact that there were test cases
                            suite["_original_test_cases_count"] = test_cases_count
                return obj

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
                msg = f"reportsmerger plugin: file {filename} does not exist and was skipped"
                display.warning(msg)
                continue

            try:
                # Use custom decoder to avoid loading heavy test_cases
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f, cls=TestSuiteOnlyDecoder)

                if "test_suites" not in data:
                    raise ValueError(f"Missing 'test_suites' field in {filename}")

                # Accumulate stats
                merged_report["time"] += float(data.get("time", 0.0))
                merged_report["tests"] += int(data.get("tests", 0))
                merged_report["failures"] += int(data.get("failures", 0))
                merged_report["errors"] += int(data.get("errors", 0))
                merged_report["skipped"] += int(data.get("skipped", 0))

                # Merge lightweight test suites
                test_suites = data.get("test_suites", [])
                merged_report["test_suites"].extend(test_suites)

                display.vv(f"Parsed {filename} (lightweight): {data.get('tests', 0)} tests")

            except Exception as e:
                msg = f"Error processing {filename}: {e}"
                display.error(msg)
                raise ValueError(msg) from e

        return merged_report
