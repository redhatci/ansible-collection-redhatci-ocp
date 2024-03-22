#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: get_compatible_rhocp_repo
author: "Farid Da Encarnacao (@fdaencarrh)"
short_description: Find the latest available RHOCP repo version by decrementing the minor version
description:
  - It is useful for finding the latest available version of the RHOCP repository.
options:
  version:
    description:
      - The version to start checking from in the format 'major.minor', e.g., '4.16'.
    required: true
    type: str
'''

EXAMPLES = '''
- name: Check repository version
  become: true
  get_compatible_rhocp_repo:
    version: "4.16"
  register: rhocp_repository_result

- debug:
    msg: "Found matching version: {{ rhocp_repository_result.version }}"
  when: rhocp_repository_result.version is defined

- debug:
    msg: "{{ rhocp_repository_result.error }}"
  when: rhocp_repository_result.error != ""
'''

RETURN = '''
version:
  description: The matching version found in the repository.
  type: str
  returned: always
  sample: "4.14"
error:
  description: Error message if an error occurred during execution.
  type: str
  returned: when an error occurs
  sample: "No matching version found."
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess


def check_repository(version):
    try:
        current_major, current_minor = map(int, version.split('.'))
    except ValueError:
        raise ValueError("Invalid version format. It should be in 'major.minor' format.")

    while current_minor >= 1:
        repository = f"rhocp-{current_major}.{current_minor}-for-rhel-9-{subprocess.check_output(['uname', '-m']).decode().strip()}-rpms"
        try:
            subprocess.run(['dnf', '-v', 'repository-packages', repository, 'info', 'cri-o'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return f"{current_major}.{current_minor}"
        except subprocess.CalledProcessError:
            current_minor -= 1
    return None


def main():
    module_args = dict(
        version=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        version=None,
        error=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    version = module.params['version']

    try:
        found_version = check_repository(version)
        if found_version is not None:
            result['version'] = found_version
            module.exit_json(**result)
        else:
            module.fail_json(msg="No matching version found.", **result)
    except Exception as e:
        module.fail_json(msg=str(e), **result)


if __name__ == '__main__':
    main()
