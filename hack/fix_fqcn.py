#!/usr/bin/env python3
"""Fix FQCN ansible-lint violations in Ansible YAML files.

This script uses YAML parsing to identify task-level module actions
and performs line-level text replacement to preserve formatting.

Handles three violation types:
1. action-core: bare ansible.builtin modules → FQCN
2. action: bare non-builtin modules → FQCN
3. canonical: incorrect FQCN → correct FQCN
"""

import os
import re
import sys

import yaml

# Mapping of bare module names to their FQCN (action-core)
BUILTIN_MODULES = {
    "add_host": "ansible.builtin.add_host",
    "assert": "ansible.builtin.assert",
    "async_status": "ansible.builtin.async_status",
    "blockinfile": "ansible.builtin.blockinfile",
    "command": "ansible.builtin.command",
    "copy": "ansible.builtin.copy",
    "cron": "ansible.builtin.cron",
    "debug": "ansible.builtin.debug",
    "dnf": "ansible.builtin.dnf",
    "fail": "ansible.builtin.fail",
    "fetch": "ansible.builtin.fetch",
    "file": "ansible.builtin.file",
    "find": "ansible.builtin.find",
    "gather_facts": "ansible.builtin.gather_facts",
    "get_url": "ansible.builtin.get_url",
    "group": "ansible.builtin.group",
    "group_by": "ansible.builtin.group_by",
    "hostname": "ansible.builtin.hostname",
    "import_role": "ansible.builtin.import_role",
    "import_tasks": "ansible.builtin.import_tasks",
    "include_role": "ansible.builtin.include_role",
    "include_tasks": "ansible.builtin.include_tasks",
    "include_vars": "ansible.builtin.include_vars",
    "iptables": "ansible.builtin.iptables",
    "known_hosts": "ansible.builtin.known_hosts",
    "lineinfile": "ansible.builtin.lineinfile",
    "meta": "ansible.builtin.meta",
    "package": "ansible.builtin.package",
    "package_facts": "ansible.builtin.package_facts",
    "pause": "ansible.builtin.pause",
    "pip": "ansible.builtin.pip",
    "raw": "ansible.builtin.raw",
    "replace": "ansible.builtin.replace",
    "script": "ansible.builtin.script",
    "service": "ansible.builtin.service",
    "set_fact": "ansible.builtin.set_fact",
    "setup": "ansible.builtin.setup",
    "shell": "ansible.builtin.shell",
    "slurp": "ansible.builtin.slurp",
    "stat": "ansible.builtin.stat",
    "systemd": "ansible.builtin.systemd",
    "systemd_service": "ansible.builtin.systemd_service",
    "tempfile": "ansible.builtin.tempfile",
    "template": "ansible.builtin.template",
    "unarchive": "ansible.builtin.unarchive",
    "uri": "ansible.builtin.uri",
    "user": "ansible.builtin.user",
    "wait_for": "ansible.builtin.wait_for",
    "yum": "ansible.builtin.yum",
    "yum_repository": "ansible.builtin.yum_repository",
    "apt": "ansible.builtin.apt",
    "service_facts": "ansible.builtin.service_facts",
    "reboot": "ansible.builtin.reboot",
    "rpm_key": "ansible.builtin.rpm_key",
    "git": "ansible.builtin.git",
    "subversion": "ansible.builtin.subversion",
    "expect": "ansible.builtin.expect",
    "getent": "ansible.builtin.getent",
    "validate_argument_spec": "ansible.builtin.validate_argument_spec",
}

# Mapping for non-builtin modules (action violations)
NON_BUILTIN_MODULES = {
    "firewalld": "ansible.posix.firewalld",
    "mount": "ansible.posix.mount",
    "seboolean": "ansible.posix.seboolean",
    "sefcontext": "community.general.sefcontext",
    "selinux": "ansible.posix.selinux",
    "synchronize": "ansible.posix.synchronize",
    "sysctl": "ansible.posix.sysctl",
    "openssl_privatekey": "community.crypto.openssl_privatekey",
    "openssl_csr": "community.crypto.openssl_csr",
    "openssl_certificate": "community.crypto.x509_certificate",
    "x509_certificate": "community.crypto.x509_certificate",
    "openssh_keypair": "community.crypto.openssh_keypair",
    "redhat_subscription": "community.general.redhat_subscription",
    "python_requirements_info": "community.general.python_requirements_info",
    "redfish_info": "community.general.redfish_info",
    "virt_pool": "community.libvirt.virt_pool",
    "htpasswd": "community.general.htpasswd",
    "ini_file": "community.general.ini_file",
    "archive": "community.general.archive",
    "nmcli": "community.general.nmcli",
    "lvg": "community.general.lvg",
    "lvol": "community.general.lvol",
    "filesystem": "community.general.filesystem",
    "parted": "community.general.parted",
    "modprobe": "community.general.modprobe",
}

# Canonical replacements: wrong FQCN → correct FQCN
CANONICAL_REPLACEMENTS = {
    "ansible.builtin.openssh_keypair": "community.crypto.openssh_keypair",
    "ansible.builtin.archive": "community.general.archive",
    "ansible.builtin.sefcontext": "community.general.sefcontext",
    "ansible.builtin.htpasswd": "community.general.htpasswd",
    "ansible.builtin.ini_file": "community.general.ini_file",
    "ansible.builtin.firewalld": "ansible.posix.firewalld",
    "ansible.builtin.mount": "ansible.posix.mount",
    "ansible.builtin.seboolean": "ansible.posix.seboolean",
    "ansible.builtin.selinux": "ansible.posix.selinux",
    "ansible.builtin.synchronize": "ansible.posix.synchronize",
    "ansible.builtin.sysctl": "ansible.posix.sysctl",
    "ansible.builtin.openssl_privatekey": "community.crypto.openssl_privatekey",
    "ansible.builtin.openssl_csr": "community.crypto.openssl_csr",
    "ansible.builtin.x509_certificate": "community.crypto.x509_certificate",
    "ansible.builtin.openssl_certificate": "community.crypto.x509_certificate",
}

# ansible.legacy.* → bare name (for DCI modules) or proper FQCN
LEGACY_REPLACEMENTS = {
    "ansible.legacy.git": "ansible.builtin.git",
    "ansible.legacy.command": "ansible.builtin.command",
    "ansible.legacy.shell": "ansible.builtin.shell",
    "ansible.legacy.copy": "ansible.builtin.copy",
    "ansible.legacy.file": "ansible.builtin.file",
    "ansible.legacy.template": "ansible.builtin.template",
    "ansible.legacy.stat": "ansible.builtin.stat",
    "ansible.legacy.set_fact": "ansible.builtin.set_fact",
    "ansible.legacy.debug": "ansible.builtin.debug",
    "ansible.legacy.fail": "ansible.builtin.fail",
    "ansible.legacy.uri": "ansible.builtin.uri",
    "ansible.legacy.include_tasks": "ansible.builtin.include_tasks",
    "ansible.legacy.import_tasks": "ansible.builtin.import_tasks",
    "ansible.legacy.setup": "ansible.builtin.setup",
    "ansible.legacy.slurp": "ansible.builtin.slurp",
    "ansible.legacy.fetch": "ansible.builtin.fetch",
    "ansible.legacy.find": "ansible.builtin.find",
    "ansible.legacy.get_url": "ansible.builtin.get_url",
    "ansible.legacy.service": "ansible.builtin.service",
    "ansible.legacy.systemd": "ansible.builtin.systemd",
    "ansible.legacy.package": "ansible.builtin.package",
    "ansible.legacy.yum": "ansible.builtin.yum",
    "ansible.legacy.dnf": "ansible.builtin.dnf",
    "ansible.legacy.pip": "ansible.builtin.pip",
    "ansible.legacy.user": "ansible.builtin.user",
    "ansible.legacy.group": "ansible.builtin.group",
    "ansible.legacy.lineinfile": "ansible.builtin.lineinfile",
    "ansible.legacy.replace": "ansible.builtin.replace",
    "ansible.legacy.unarchive": "ansible.builtin.unarchive",
    "ansible.legacy.tempfile": "ansible.builtin.tempfile",
    "ansible.legacy.iptables": "ansible.builtin.iptables",
    "ansible.legacy.wait_for": "ansible.builtin.wait_for",
    "ansible.legacy.add_host": "ansible.builtin.add_host",
    "ansible.legacy.pause": "ansible.builtin.pause",
    "ansible.legacy.assert": "ansible.builtin.assert",
    "ansible.legacy.meta": "ansible.builtin.meta",
    "ansible.legacy.raw": "ansible.builtin.raw",
}

# All known task-level keys that are NOT module names
TASK_KEYWORDS = {
    "name", "when", "register", "tags", "vars", "loop", "with_items",
    "with_dict", "with_list", "with_fileglob", "with_first_found",
    "with_together", "with_sequence", "with_random_choice",
    "with_subelements", "with_nested", "with_indexed_items",
    "with_flattened", "with_inventory_hostnames", "with_lines",
    "until", "retries", "delay", "changed_when", "failed_when",
    "become", "become_user", "become_method", "become_flags",
    "environment", "ignore_errors", "ignore_unreachable",
    "no_log", "delegate_to", "delegate_facts", "run_once",
    "connection", "collections", "module_defaults", "block",
    "rescue", "always", "notify", "listen", "handler",
    "check_mode", "diff", "any_errors_fatal", "throttle",
    "timeout", "loop_control", "async", "poll", "args",
}


def find_yaml_files(base_dirs, exclude_dirs=None):
    """Find all YAML files in given directories, excluding specified dirs."""
    if exclude_dirs is None:
        exclude_dirs = {"molecule", ".ansible"}
    yaml_files = []
    for base_dir in base_dirs:
        if not os.path.isdir(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                if f.endswith((".yml", ".yaml")):
                    yaml_files.append(os.path.join(root, f))
    return sorted(yaml_files)


def get_task_module_locations(filepath):
    """Parse YAML and return set of (line_number, module_name) tuples.

    Uses yaml.compose_all() to obtain MappingNode start_mark.line for each
    task-level action key, so that fix_file() can scope rewrites to the
    exact lines where modules are invoked (avoiding false positives on
    parameter keys like ``group:`` inside an ``ansible.builtin.file`` task).

    Line numbers are 1-based to match enumerate(lines, 1).
    """
    try:
        with open(filepath) as f:
            content = f.read()
    except (IOError, OSError):
        return set()

    try:
        nodes = list(yaml.compose_all(content))
    except yaml.YAMLError:
        return set()

    locations = set()

    def process_task_node(node):
        """Extract (line_number, module_name) from a task MappingNode."""
        if not isinstance(node, yaml.MappingNode):
            return
        for key_node, _value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode):
                continue
            key = key_node.value
            if key in TASK_KEYWORDS:
                continue
            if (key in BUILTIN_MODULES or key in NON_BUILTIN_MODULES
                    or key.startswith("ansible.") or "." in key):
                # start_mark.line is 0-based; store as 1-based
                locations.add((key_node.start_mark.line + 1, key))

    def process_tasks_list_node(node):
        """Process a SequenceNode of tasks."""
        if not isinstance(node, yaml.SequenceNode):
            return
        for item in node.value:
            if not isinstance(item, yaml.MappingNode):
                continue
            process_task_node(item)
            for key_node, value_node in item.value:
                if not isinstance(key_node, yaml.ScalarNode):
                    continue
                # Handle block/rescue/always
                if key_node.value in ("block", "rescue", "always"):
                    process_tasks_list_node(value_node)
                # Descend into play task sections (list-of-plays case)
                if key_node.value in ("tasks", "pre_tasks",
                                      "post_tasks", "handlers"):
                    process_tasks_list_node(value_node)

    for node in nodes:
        if isinstance(node, yaml.SequenceNode):
            process_tasks_list_node(node)
        elif isinstance(node, yaml.MappingNode):
            # Could be a playbook with task sections
            for key_node, value_node in node.value:
                if isinstance(key_node, yaml.ScalarNode):
                    if key_node.value in ("tasks", "pre_tasks",
                                          "post_tasks", "handlers"):
                        process_tasks_list_node(value_node)
            # Could be a single task
            process_task_node(node)

    return locations


def fix_file(filepath, dry_run=False):
    """Fix FQCN violations in a single file."""
    try:
        with open(filepath) as f:
            original_lines = f.readlines()
    except (IOError, OSError) as e:
        print(f"  Error reading {filepath}: {e}")
        return 0

    # Get (line_number, module_name) tuples for task-level actions
    task_action_locations = get_task_module_locations(filepath)

    lines = list(original_lines)
    changes = 0

    for i, line in enumerate(lines):
        line_no = i + 1  # 1-based to match task_action_locations
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = line[:len(line) - len(stripped)]
        new_line = line

        # 1. Fix canonical violations: ansible.builtin.X → correct FQCN
        for wrong_fqcn, correct_fqcn in CANONICAL_REPLACEMENTS.items():
            pattern = f"{wrong_fqcn}:"
            if stripped.startswith(pattern):
                new_line = f"{indent}{correct_fqcn}:{stripped[len(pattern):]}"
                if not new_line.endswith("\n"):
                    new_line += "\n"
                break

        # 2. Fix legacy violations: ansible.legacy.X → correct FQCN or bare name
        for legacy, replacement in LEGACY_REPLACEMENTS.items():
            pattern = f"{legacy}:"
            if stripped.startswith(pattern):
                new_line = f"{indent}{replacement}:{stripped[len(pattern):]}"
                if not new_line.endswith("\n"):
                    new_line += "\n"
                break

        # 3. Fix action-core: bare builtin module → FQCN
        # Only fix if this exact line was identified as a task-level action
        for bare, fqcn in BUILTIN_MODULES.items():
            pattern = f"{bare}:"
            if (stripped.startswith(pattern)
                    and (line_no, bare) in task_action_locations):
                # Don't replace if it's already FQCN
                if not stripped.startswith(f"ansible.builtin.{bare}:"):
                    new_line = f"{indent}{fqcn}:{stripped[len(pattern):]}"
                    if not new_line.endswith("\n"):
                        new_line += "\n"
                break

        # 4. Fix action: bare non-builtin module → FQCN
        for bare, fqcn in NON_BUILTIN_MODULES.items():
            pattern = f"{bare}:"
            if (stripped.startswith(pattern)
                    and (line_no, bare) in task_action_locations):
                # Don't replace if already has dots (already FQCN)
                if "." not in bare:
                    new_line = f"{indent}{fqcn}:{stripped[len(pattern):]}"
                    if not new_line.endswith("\n"):
                        new_line += "\n"
                break

        if new_line != line:
            lines[i] = new_line
            changes += 1

    if changes > 0 and not dry_run:
        with open(filepath, "w") as f:
            f.writelines(lines)
        print(f"  Fixed {changes} violations in {filepath}")

    return changes


def main():
    """Main entry point."""
    dry_run = "--dry-run" in sys.argv

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_dirs = [
        os.path.join(base_dir, "roles"),
        os.path.join(base_dir, "playbooks"),
    ]

    yaml_files = find_yaml_files(search_dirs)
    print(f"Found {len(yaml_files)} YAML files to check")

    total_changes = 0
    files_changed = 0

    for filepath in yaml_files:
        changes = fix_file(filepath, dry_run=dry_run)
        if changes > 0:
            total_changes += changes
            files_changed += 1

    print(f"\nTotal: {total_changes} fixes in {files_changed} files")
    if dry_run:
        print("(dry run - no files were modified)")


if __name__ == "__main__":
    main()
