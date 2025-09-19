#
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

__metaclass__ = type
from ansible_collections.redhatci.ocp.plugins.filter import redact


class TestRedactFilter:
    def test_redact_basic_auth_field(self):
        """Test basic redaction of auth field with default parameters"""
        data = {"auth": "secret_token", "name": "test"}
        result = redact.redact(data)
        expected = {"auth": "REDACTED", "name": "test"}
        assert result == expected

    def test_redact_case_insensitive(self):
        """Test that redaction is case insensitive"""
        data = {"AUTH": "secret", "Auth": "token", "auth": "password"}
        result = redact.redact(data, fields="auth")
        expected = {"AUTH": "REDACTED", "Auth": "REDACTED", "auth": "REDACTED"}
        assert result == expected

    def test_redact_custom_fields(self):
        """Test redaction with custom field list"""
        data = {"password": "secret", "token": "abc123", "name": "test"}
        result = redact.redact(data, fields="password,token")
        expected = {"password": "REDACTED", "token": "REDACTED", "name": "test"}
        assert result == expected

    def test_redact_empty_dictionary(self):
        """Test redaction with empty dictionary"""
        data = {}
        result = redact.redact(data, fields="auth")
        expected = {}
        assert result == expected

    def test_redact_non_dictionary(self):
        """Test redaction with empty dictionary"""
        data = "just a string"
        result = redact.redact(data, fields="auth")
        expected = "just a string"
        assert result == expected

    def test_redact_no_matching_fields(self):
        """Test redaction when no fields match"""
        data = {"name": "test", "value": "data"}
        result = redact.redact(data, fields="auth,password")
        expected = {"name": "test", "value": "data"}
        assert result == expected

    def test_redact_fields_with_spaces(self):
        """Test redaction with fields containing spaces in CSV"""
        data = {"auth": "secret", "token": "abc123", "name": "test"}
        result = redact.redact(data, fields=" auth , token ")
        expected = {"auth": "REDACTED", "token": "REDACTED", "name": "test"}
        assert result == expected

    def test_redact_deeply_nested_structure(self):
        """Test redaction in deeply nested structures"""
        data = {
            "level1": {"auth": "secret1", "level2": {"auth": "secret2", "level3": {"auth": "secret3", "name": "deep"}}}
        }
        result = redact.redact(data, fields="auth")
        expected = {
            "level1": {
                "auth": "REDACTED",
                "level2": {"auth": "REDACTED", "level3": {"auth": "REDACTED", "name": "deep"}},
            }
        }
        assert result == expected

    def test_redact_complex_nested_with_lists(self):
        """Test redaction in complex nested structure with lists and dicts"""
        data = {
            "auth": "main_secret",
            "servers": [
                {
                    "auth": "server1_secret",
                    "configs": [
                        {"auth": "config1_secret", "name": "config1"},
                        {"auth": "config2_secret", "name": "config2"},
                        {"auth": {"auth": "config3_secret", "name": "config3"}},
                    ],
                },
                {"auth": "server2_secret", "name": "server2"},
            ],
        }
        result = redact.redact(data, fields="auth")
        expected = {
            "auth": "REDACTED",
            "servers": [
                {
                    "auth": "REDACTED",
                    "configs": [
                        {"auth": "REDACTED", "name": "config1"},
                        {"auth": "REDACTED", "name": "config2"},
                        {"auth": "REDACTED"},
                    ],
                },
                {"auth": "REDACTED", "name": "server2"},
            ],
        }
        assert result == expected


class TestFilterModule:
    def test_filter_module_returns_redact_filter(self):
        """Test that FilterModule properly exposes the redact filter"""
        filter_module = redact.FilterModule()
        filters = filter_module.filters()
        assert "redact" in filters
        assert filters["redact"] == redact.redact

    def test_filter_module_can_be_called(self):
        """Test that the filter can be called through FilterModule"""
        filter_module = redact.FilterModule()
        filters = filter_module.filters()
        redact_func = filters["redact"]

        data = {"auth": "secret", "name": "test"}
        result = redact_func(data, fields="auth")
        expected = {"auth": "REDACTED", "name": "test"}
        assert result == expected
