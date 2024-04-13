# Copyright (C) 2024 Red Hat, Inc.
#
# Author: Jorge A Gallegos <jgallego@redhat.com>
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
"""
Specific rule definitions for coding conventions in Redhat CI
"""

import logging

from ansiblelint.constants import ANNOTATION_KEYS, LINE_NUMBER_KEY
from ansiblelint.errors import MatchError
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.text import has_jinja
from ansiblelint.utils import Lintable, Task

_logger = logging.getLogger(__name__)


class CollectionNamingConvention(AnsibleLintRule):
    """Rules for the RedHat OCP Collection naming convention"""

    id = "redhat-ci"
    description = "RedHat OCP Collection naming convention"
    severity = "MEDIUM"
    tags = ["experimental", "idiom", "redhat"]
    varsion_added = "historic"
    needs_raw_task = True
    # These special variables are used by Ansible but we allow users to set
    # them as they might need it in certain cases.
    allowed_special_names = {
        "ansible_facts",
        "ansible_become_user",
        "ansible_connection",
        "ansible_host",
        "ansible_python_interpreter",
        "ansible_user",
        "ansible_remote_tmp",  # no included in docs
    }

    def get_var_naming_matcherror(
        self, ident: str, *, role: str, private: bool = False
    ) -> MatchError | None:
        """Return a MatchError if the variable name doesn't match prefix."""

        # don't try to match private keys
        if ident.startswith("__") and ident.endswith("__"):
            return None

        # don't try to match special names either
        if ident in ANNOTATION_KEYS or ident in self.allowed_special_names:
            return None

        # if the role is templated, we can't possibly know what prefix to use
        if has_jinja(role):
            _logger.warning(f"Role name is templated, can't analyze (role: {role})")
            return None

        # finally, if we can't figure out the role name we can't figure out the
        # prefix
        if role.strip() == "":
            _logger.debug(f"Passed empty role name for {ident}")
            return None

        #####################
        # PREFIX HEURISTICS #
        # vvvvvvvvvvvvvvvvv #
        #####################
        possible_prefix = set()
        # https://www.researchgate.net/figure/Average-word-length-in-the-English-language-Different-colours-indicate-the-results-for_fig1_230764201
        SHORT = 6
        # compute the prefix
        # if the role name is really short, just use the role name as prefix
        if len(role) < SHORT:
            computed_prefix = role
        else:
            parts = role.split("_")
            if len(parts) == 1:
                # if it's a single word, use the first few chars from it
                computed_prefix = parts[0][:SHORT]
            else:
                # else, use an acronym
                computed_prefix = "".join(_[0] for _ in parts)

        # registering within roles should require "privatizing" variables
        if private:
            possible_prefix.add(f"_{role}")
            possible_prefix.add(f"_{computed_prefix}")
        else:
            possible_prefix.add("global")
            possible_prefix.add(f"{role}")
            possible_prefix.add(f"{computed_prefix}")

        #####################
        # ^^^^^^^^^^^^^^^^^ #
        # PREFIX HEURISTICS #
        #####################

        # If variable starts with any of the allowed prefixes, this is a valid
        # variable name
        for prefix in possible_prefix:
            if ident.startswith(f"{prefix}_"):
                return None

        # fail if the task didnt' start with any of the allowed prefixes
        return MatchError(
            tag="redhat-ci[no-role-prefix]",
            message="Variable names from within roles "
            + "should use a prefix related to the role. "
            + f"({possible_prefix} are possible)",
            rule=self,
        )

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> list[MatchError]:
        """Return matches for task based variables."""
        results: list[MatchError] = []
        ansible_module = task["action"]["__ansible_module__"]

        filename = "" if file is None else str(file.path)
        role_name = ""
        if file and file.parent and file.parent.kind == "role":
            role_name = file.parent.path.name

        # If we're importing roles/tasks
        if ansible_module in (
            "include_role",
            "import_role",
            "include_tasks",
            "import_tasks",
        ):
            # If the task uses the 'vars' section to set variables
            our_vars = task.get("vars", {})
            for key in our_vars:
                match_error = self.get_var_naming_matcherror(key, role=role_name)
                if match_error:
                    match_error.filename = filename
                    match_error.lineno = our_vars[LINE_NUMBER_KEY]
                    match_error.message += f" (vars: {key})"
                    results.append(match_error)

        # If the task uses the 'set_fact' module
        if ansible_module == "set_fact":
            for key in filter(
                lambda x: isinstance(x, str)
                and not x.startswith("__")
                and x != "cacheable",
                task["action"].keys(),
            ):
                match_error = self.get_var_naming_matcherror(key, role=role_name)
                if match_error:
                    match_error.filename = filename
                    match_error.lineno = task["action"][LINE_NUMBER_KEY]
                    match_error.message += f" (set_fact: {key})"
                    results.append(match_error)

        # If the task registers a variable
        registered_var = task.get("register", None)
        if registered_var:
            match_error = self.get_var_naming_matcherror(
                registered_var, role=role_name, private=True
            )
            if match_error:
                match_error.message += f" (register: {registered_var})"
                match_error.filename = filename
                match_error.lineno = task[LINE_NUMBER_KEY]
                results.append(match_error)

        return results
