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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import tempfile
import unittest

from ansible_collections.redhatci.ocp.plugins.filter import ocp_compatibility


class TestOcpCompatibility(unittest.TestCase):
    def test_filter(self):
        filter = ocp_compatibility.FilterModule()
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.assertEqual(
                filter.filters()["ocp_compatibility"](
                    [], "4.15", os.path.join(tmpdirname, "junit.xml")
                ),
                {"4.15": "compatible", "4.16": "compatible"},
            )


if __name__ == "__main__":
    unittest.main()

# test_ocp_compatibility.py ends here
