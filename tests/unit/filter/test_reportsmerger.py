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

    # Compare with expected result (accounting for schema version difference)
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_data_object[key] == actual[key]
    assert actual["schema_version"] == "1.1.0"


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

    # Compare with expected result from static file (accounting for schema version)
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_result[key] == result[key]
    assert result["schema_version"] == "1.1.0"


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

    # Compare with expected result from static file (accounting for schema version)
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_result[key] == result[key]
    assert result["schema_version"] == "1.1.0"


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


# New tests for strategy parameter
def test_reportsmerger_strategy_validation():
    """Test strategy parameter validation"""
    filter_plugin = reportsmerger.FilterModule()

    # Test invalid strategy
    with pytest.raises(ValueError, match="Invalid strategy 'invalid'"):
        filter_plugin.filters()["reportsmerger"](
            ["tests/unit/data/test_reportsmerger_input1.json"],
            strategy="invalid"
        )


@pytest.mark.parametrize("strategy", ["normal", "large", "many"])
def test_reportsmerger_compatible_strategies(strategy, json_loader):
    """Test that compatible strategies produce equivalent results for simple case"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = ["tests/unit/data/test_reportsmerger_input1.json"]
    expected_data = "tests/unit/data/test_reportsmerger_single_result.json"
    expected_result = json_loader(expected_data)

    # Test each strategy
    actual = filter_plugin.filters()["reportsmerger"](input_files, strategy=strategy)

    # These strategies should produce equivalent results (except schema_version)
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_result[key] == actual[key]

    # Schema version will be different (1.1.0 vs 1.0.0)
    assert actual["schema_version"] == "1.1.0"


def test_reportsmerger_strategy_large_streaming(json_loader):
    """Test large strategy specifically for memory efficiency"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = [
        "tests/unit/data/test_reportsmerger_input1.json",
        "tests/unit/data/test_reportsmerger_input2.json",
    ]
    expected_data = "tests/unit/data/test_reportsmerger_multi_result.json"
    expected_result = json_loader(expected_data)

    actual = filter_plugin.filters()["reportsmerger"](input_files, strategy="large")

    # Compare all fields except schema_version
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_result[key] == actual[key]
    assert actual["schema_version"] == "1.1.0"


def test_reportsmerger_strategy_many_parallel(json_loader):
    """Test many strategy specifically for parallel processing"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = [
        "tests/unit/data/test_reportsmerger_input1.json",
        "tests/unit/data/test_reportsmerger_input2.json",
    ]
    expected_data = "tests/unit/data/test_reportsmerger_multi_result.json"
    expected_result = json_loader(expected_data)

    actual = filter_plugin.filters()["reportsmerger"](input_files, strategy="many")

    # Compare all fields except schema_version
    for key in ["time", "tests", "failures", "errors", "skipped"]:
        assert expected_result[key] == actual[key]

    # For parallel processing, test_suites order might differ, so sort by name for comparison
    expected_suites = sorted(expected_result["test_suites"], key=lambda x: x["name"])
    actual_suites = sorted(actual["test_suites"], key=lambda x: x["name"])
    assert expected_suites == actual_suites

    assert actual["schema_version"] == "1.1.0"


def test_reportsmerger_strategy_shallow_lazy(json_loader):
    """Test shallow strategy with lazy test suites loading"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = ["tests/unit/data/test_reportsmerger_input1.json"]
    expected_data = "tests/unit/data/test_reportsmerger_single_result.json"
    expected_result = json_loader(expected_data)

    actual = filter_plugin.filters()["reportsmerger"](input_files, strategy="shallow")

    # Stats should match (except schema_version)
    for key in ["time", "tests", "failures", "errors", "skipped"]:
        assert expected_result[key] == actual[key]
    assert actual["schema_version"] == "1.1.0"

    # Test suites should be lazy-loaded but equivalent when accessed
    assert len(actual["test_suites"]) == len(expected_result["test_suites"])
    assert list(actual["test_suites"]) == expected_result["test_suites"]


def test_reportsmerger_strategy_complex_parsing(json_loader):
    """Test complex strategy with schema-specific parsing"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = ["tests/unit/data/test_reportsmerger_input1.json"]
    expected_data = "tests/unit/data/test_reportsmerger_single_result.json"
    expected_result = json_loader(expected_data)

    actual = filter_plugin.filters()["reportsmerger"](input_files, strategy="complex")

    # Stats should match exactly (except schema_version)
    for key in ["time", "tests", "failures", "errors", "skipped"]:
        assert expected_result[key] == actual[key]
    assert actual["schema_version"] == "1.1.0"

    # Test suites should have empty test_cases (complex strategy optimization)
    assert len(actual["test_suites"]) == len(expected_result["test_suites"])
    for suite in actual["test_suites"]:
        assert suite["test_cases"] == []  # Should be empty due to complex parsing
        # But should have the count preserved
        if "_original_test_cases_count" in suite:
            assert suite["_original_test_cases_count"] >= 0


def test_reportsmerger_default_strategy_backward_compatibility(json_loader):
    """Test that default behavior (no strategy param) works as before"""
    filter_plugin = reportsmerger.FilterModule()

    input_files = ["tests/unit/data/test_reportsmerger_input1.json"]
    expected_data = "tests/unit/data/test_reportsmerger_single_result.json"
    expected_result = json_loader(expected_data)

    # Test without strategy parameter (should default to "normal")
    actual_default = filter_plugin.filters()["reportsmerger"](input_files)
    actual_normal = filter_plugin.filters()["reportsmerger"](input_files, strategy="normal")

    # Both should be identical
    assert actual_default == actual_normal

    # Compare with expected result (accounting for schema version difference)
    for key in ["time", "tests", "failures", "errors", "skipped", "test_suites"]:
        assert expected_result[key] == actual_default[key]
    assert actual_default["schema_version"] == "1.1.0"
