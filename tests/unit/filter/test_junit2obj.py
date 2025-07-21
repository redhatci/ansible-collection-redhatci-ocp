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
import json
import pytest
try:
    from ansible_collections.redhatci.ocp.plugins.filter import junit2obj
except ImportError:
    from plugins.filter import junit2obj


@pytest.fixture
def input_data(request):  # type: ignore
    file_path: str = str(request.param)  # type: ignore
    with open(file_path, "r") as fd:
        return fd.read()


@pytest.fixture
def expected_data_object(request):  # type: ignore
    file_path: str = str(request.param)  # type: ignore
    with open(file_path, "r") as fd:
        return json.loads(fd.read())


@pytest.mark.parametrize(
    "input_data,expected_data_object",
    [
        (
            "tests/unit/data/test_junit2obj_simple_single_input.xml",
            "tests/unit/data/test_junit2obj_simple_result.json",
        ),
        (
            "tests/unit/data/test_junit2obj_simple_input.xml",
            "tests/unit/data/test_junit2obj_simple_result.json",
        ),
        (
            "tests/unit/data/test_junit2obj_failure_input.xml",
            "tests/unit/data/test_junit2obj_failure_result.json",
        ),
        (
            "tests/unit/data/test_junit2obj_complex_input.xml",
            "tests/unit/data/test_junit2obj_complex_result.json",
        ),
    ],
    indirect=True,
)
def test_simple_data_object_true(input_data, expected_data_object):  # type: ignore
    filter = junit2obj.FilterModule()
    actual: str = filter.filters()["junit2obj"](input_data)  # type: ignore
    assert expected_data_object == actual
