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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import json
import pytest
from unittest.mock import patch, MagicMock
# TODO: reconcile current data conversion and pass it using the CI
from ansible_collections.redhatci.ocp.plugins.filter import reportsmerger


@pytest.fixture
def json_loader():
    """Factory fixture that returns a function to load JSON from file paths"""
    def _load_json_file(file_path: str):
        with open(file_path, "r") as fd:
            return json.loads(fd.read())
    return _load_json_file


@pytest.fixture
def expected_data_object(request, json_loader):  # type: ignore
    """Load expected data using the json_loader fixture"""
    file_path: str = str(request.param)  # type: ignore
    return json_loader(file_path)


@pytest.mark.parametrize(
    "input_files,expected_data_object",
    [
        # Single file test
        (
            [
                "tests/unit/data/test_reportsmerger_input1.json",
            ],
            "tests/unit/data/test_reportsmerger_single_result.json",
        ),
        # Multiple files test
        (
            [
                "tests/unit/data/test_reportsmerger_input1.json",
                "tests/unit/data/test_reportsmerger_input2.json",
            ],
            "tests/unit/data/test_reportsmerger_multi_result.json",
        ),
        # None values test
        (
            [
                "tests/unit/data/test_reportsmerger_none_input.json",
            ],
            "tests/unit/data/test_reportsmerger_none_result.json",
        ),
        # Mixed existing files test (valid files only, ignoring missing ones)
        (
            [
                "tests/unit/data/test_reportsmerger_mixed_valid.json",
            ],
            "tests/unit/data/test_reportsmerger_mixed_result.json",
        ),
    ],
    indirect=["expected_data_object"],
)
def test_reportsmerger_with_static_data(input_files, expected_data_object):  # type: ignore
    """Test reportsmerger filter with static test data files"""
    filter_plugin = reportsmerger.FilterModule()

    # Test the filter with the input files (reportsmerger expects file paths)
    actual = filter_plugin.filters()["reportsmerger"](input_files)  # type: ignore

    # Compare with expected result (loaded via json_loader fixture)
    assert expected_data_object == actual


def test_reportsmerger_empty_list():
    """Test error handling for empty file list"""
    filter_plugin = reportsmerger.FilterModule()

    with pytest.raises(ValueError, match="requires at least one filename"):
        filter_plugin.filters()["reportsmerger"]([])


def test_reportsmerger_invalid_input():
    """Test error handling for non-list input"""
    filter_plugin = reportsmerger.FilterModule()

    with pytest.raises(TypeError, match="expects a list of filenames"):
        filter_plugin.filters()["reportsmerger"]("not_a_list")


def test_reportsmerger_missing_file(json_loader):
    """Test handling of missing files (should emit warning and skip)"""
    filter_plugin = reportsmerger.FilterModule()

    expected_data: str = "tests/unit/data/test_reportsmerger_empty_result.json"
    # Load expected empty result using json_loader fixture
    expected_result = json_loader(expected_data)

    # Mock the Display class to capture warning calls
    with patch('ansible_collections.redhatci.ocp.plugins.filter.reportsmerger.Display') as mock_display_class:
        mock_display = MagicMock()
        mock_display_class.return_value = mock_display

        fname: str = "nonexistent_file.json"
        # Test with only missing files - should return empty result
        result = filter_plugin.filters()["reportsmerger"]([fname])

        # Verify warning was called with correct message
        mock_display.warning.assert_called_once_with(
            f"reportsmerger plugin: file {fname} does not exist and was skipped"
        )

    # Compare with expected result from static file
    assert expected_result == result


def test_reportsmerger_mixed_existing_missing_files(json_loader):
    """Test handling of mix of existing and missing files"""
    filter_plugin = reportsmerger.FilterModule()

    # Use static test data files
    valid_file: str = "tests/unit/data/test_reportsmerger_mixed_valid.json"
    expected_data: str = "tests/unit/data/test_reportsmerger_mixed_result.json"
    # Load expected result using json_loader fixture
    expected_result = json_loader(expected_data)

    # Mock the Display class to capture warning calls
    with patch('ansible_collections.redhatci.ocp.plugins.filter.reportsmerger.Display') as mock_display_class:
        mock_display = MagicMock()
        mock_display_class.return_value = mock_display
        fname = "nonexistent"
        missing_files_list = [f"{fname}{i}.json" for i in range(1, 3)]
        files_list = missing_files_list + [valid_file]
        # Test with mix of existing and missing files
        result = filter_plugin.filters()["reportsmerger"](files_list)
        # Verify warnings were called for missing files
        expected_warnings = [f"reportsmerger plugin: file {f} does not exist and was skipped" for f in missing_files_list]

        assert mock_display.warning.call_count == len(missing_files_list)
        actual_warning_calls = [call[0][0] for call in mock_display.warning.call_args_list]
        assert actual_warning_calls == expected_warnings

    # Compare with expected result from static file
    assert expected_result == result


def test_reportsmerger_invalid_json(json_loader):
    """Test error handling for invalid JSON"""
    filter_plugin = reportsmerger.FilterModule()

    # Use static invalid JSON file
    test_file: str = "tests/unit/data/test_reportsmerger_invalid.not_json"

    with pytest.raises(ValueError, match="Invalid JSON"):
        filter_plugin.filters()["reportsmerger"]([test_file])


def test_reportsmerger_missing_test_suites(json_loader):
    """Test error handling for missing test_suites field"""
    filter_plugin = reportsmerger.FilterModule()

    # Use static file with missing test_suites field
    test_file: str = "tests/unit/data/test_reportsmerger_missing_test_suites.json"

    with pytest.raises(ValueError, match="Missing 'test_suites' field"):
        filter_plugin.filters()["reportsmerger"]([test_file])
