#
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
# import json
import pytest

# TODO: reconcile current data conversion and pass it using the CI
from ansible_collections.redhatci.ocp.plugins.filter import junit2obj


@pytest.fixture
def input_data(request):  # type: ignore
    file_path: str = str(request.param)  # type: ignore
    with open(file_path, "r") as fd:
        return fd.read()


@pytest.fixture
def expected_data(request):  # type: ignore
    file_path: str = str(request.param)  # type: ignore
    with open(file_path, "r") as fd:
        return fd.read()


@pytest.mark.parametrize(
    "input_data,expected_data",
    [
        (
            "tests/unit/data/test_junit2dict_simple_input.xml",
            "tests/unit/data/test_junit2dict_simple_result.json",
        ),
        (
            "tests/unit/data/test_junit2dict_failure_input.xml",
            "tests/unit/data/test_junit2dict_failure_result.json",
        ),
        (
            "tests/unit/data/test_junit2dict_complex_input.xml",
            "tests/unit/data/test_junit2dict_complex_result.json",
        ),
    ],
    indirect=True,
)
def test_simple_data(input_data, expected_data):  # type: ignore
    filter = junit2obj.FilterModule()
    actual: str = filter.filters()["junit2obj"](input_data)  # type: ignore
    assert expected_data == actual
