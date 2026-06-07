#
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.redhatci.ocp.plugins.filter import cmdline_to_json


class TestCmdlineToJson:
    def test_basic_key_value(self):
        """Test basic key=value parsing"""
        result = json.loads(cmdline_to_json.cmdline_to_json("root=/dev/sda1"))
        assert result == {"root": "/dev/sda1"}

    def test_multiple_key_value(self):
        """Test multiple key=value pairs"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("root=/dev/sda1 console=ttyS0")
        )
        assert result == {"root": "/dev/sda1", "console": "ttyS0"}

    def test_bare_flags(self):
        """Test bare flags without values"""
        result = json.loads(cmdline_to_json.cmdline_to_json("ro quiet"))
        assert result == {"ro": "", "quiet": ""}

    def test_mixed_flags_and_values(self):
        """Test mix of bare flags and key=value pairs"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("ro root=/dev/sda1 quiet")
        )
        assert result == {"ro": "", "root": "/dev/sda1", "quiet": ""}

    def test_dot_separated_nested_keys(self):
        """Test dot-separated keys create nested dictionaries"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("systemd.unit=multi-user.target")
        )
        assert result == {"systemd": {"unit": "multi-user.target"}}

    def test_deeply_nested_dot_keys(self):
        """Test deeply nested dot-separated keys"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("a.b.c=value")
        )
        assert result == {"a": {"b": {"c": "value"}}}

    def test_comma_separated_values(self):
        """Test comma-separated values are split into lists"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("isolcpus=1,2,3")
        )
        assert result == {"isolcpus": ["1", "2", "3"]}

    def test_boot_image_exception(self):
        """Test BOOT_IMAGE with commas is NOT split"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json(
                "BOOT_IMAGE=(hd0,gpt2)/vmlinuz-5.14.0"
            )
        )
        assert result == {"BOOT_IMAGE": "(hd0,gpt2)/vmlinuz-5.14.0"}

    def test_empty_input(self):
        """Test empty string input returns empty JSON object"""
        result = json.loads(cmdline_to_json.cmdline_to_json(""))
        assert result == {}

    def test_default_argument(self):
        """Test calling without arguments uses default empty string"""
        result = json.loads(cmdline_to_json.cmdline_to_json())
        assert result == {}

    def test_full_cmdline(self):
        """Test a realistic full kernel command line"""
        cmdline = (
            "BOOT_IMAGE=(hd0,gpt2)/vmlinuz-5.14.0-362.el9.x86_64 "
            "root=/dev/mapper/rhel-root ro crashkernel=1G-4G:192M,4G-64G:256M "
            "resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root "
            "rd.lvm.lv=rhel/swap quiet"
        )
        result = json.loads(cmdline_to_json.cmdline_to_json(cmdline))

        assert result["BOOT_IMAGE"] == "(hd0,gpt2)/vmlinuz-5.14.0-362.el9.x86_64"
        assert result["root"] == "/dev/mapper/rhel-root"
        assert result["ro"] == ""
        assert result["quiet"] == ""
        # crashkernel has commas so it becomes a list
        assert isinstance(result["crashkernel"], list)
        assert result["crashkernel"] == ["1G-4G:192M", "4G-64G:256M"]
        # resume is a plain key=value
        assert result["resume"] == "/dev/mapper/rhel-swap"
        # rd.lvm.lv uses dot notation -> nested dict
        assert result["rd"]["lvm"]["lv"] == "rhel/swap"

    def test_value_with_equals_sign(self):
        """Test value containing an equals sign"""
        result = json.loads(
            cmdline_to_json.cmdline_to_json("key=val=ue")
        )
        assert result == {"key": "val=ue"}


class TestFilterModule:
    def test_filter_module_returns_cmdline_to_json_filter(self):
        """Test that FilterModule properly exposes the filter"""
        filter_module = cmdline_to_json.FilterModule()
        filters = filter_module.filters()
        assert "cmdline_to_json" in filters
        assert filters["cmdline_to_json"] == cmdline_to_json.cmdline_to_json

    def test_filter_module_can_be_called(self):
        """Test that the filter can be called through FilterModule"""
        filter_module = cmdline_to_json.FilterModule()
        filters = filter_module.filters()
        func = filters["cmdline_to_json"]

        result = json.loads(func("key=value"))
        assert result == {"key": "value"}
