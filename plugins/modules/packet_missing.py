#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: packet_missing

short_description: Organize packet missing events

version_added: "2.9"

description:
    - Organize the packet missing and recovery events to find packet loss

options:
    matched:
        description:
            - K8S Event resource list for packet matches
        required: true
        type: list
    dropped:
        description:
            - K8S Event resource list for packet dropped
        required: true
        type: list
    strict:
        description:
            - Whether to uset strict checking on events or ignore short differences
        required: false
        type: bool
        default: false

author:
    - Saravanan KR (@krsacme)
'''

EXAMPLES = '''
# Parse event list
- name: prase event list
  packet_missing:
    matched: []
    dropped: []
    strict: no

'''

RETURN = '''
message:
    description: The output message that the test module generates
    type: str
    returned: always
missing:
    description: List of instances where the packet missing is observed
    type: list
    returned: always
'''

import traceback

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.basic import AnsibleModule

try:
    from dateutil.parser import parse
except ImportError:
    HAS_PARSE = False
    PARSE_ERROR = traceback.format_exc()
else:
    HAS_PARSE = True
    PARSE_ERROR = None


def get_missing_list(module, result):

    matched = module.params['matched']
    dropped = module.params['dropped']
    strict = module.params['strict']
    combine = sorted(matched + dropped, key=lambda x: parse(x['eventTime']))
    result['count'] = len(combine)
    if len(combine) < 2:
        result['message'] = "Event list length is lesser thatn 2"
        return False
    if combine[0]['reason'] == 'PacketMatched':
        del combine[0]
    if combine[0]['reason'] != 'PacketDropped':
        result['message'] = "First event should be dropped"
        return False

    missing = []
    for i in range(0, len(combine), 2):
        if combine[i]['reason'] != 'PacketDropped' and len(combine) > (i + 1):
            result['warning'] = ("Resson %s is not valid" % combine[i]['reason'])
            if combine[i + 1]['reason'] == 'PacketDropped':
                del combine[i]
            continue

        # Handle when the last event is PacketDropped (no recovery event)
        if len(combine) == (i + 1):
            missing.append({'start': combine[i]['eventTime'], 'duration': -1})
            result['warning'] = "Last event is dropped"
            break

        if combine[i + 1]['reason'] != 'PacketMatched':
            result['message'] = ("Reason %s is not valid for followed event" % combine[i + 1]['reason'])
            return False

        dropped_time = parse(combine[i]['eventTime'])
        matched_time = parse(combine[i + 1]['eventTime'])
        diff = matched_time - dropped_time
        diff_seconds = diff.total_seconds()
        if not strict and int(diff_seconds) <= 1:
            continue
        obj = {}
        obj['start'] = combine[i]['eventTime']
        obj['duration'] = diff_seconds
        missing.append(obj)

    result['missing'] = missing
    if missing:
        result['message'] = "Packet miss found"
    elif not strict and missing:
        result['message'] = "No packet miss during migration"
    else:
        result["message"] = "No packet miss"
    return True


def run_module():
    module_args = dict(
        matched=dict(type='list', required=True),
        dropped=dict(type='list', required=True),
        strict=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        missing=[],
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if not HAS_PARSE:
        module.fail_json(
            msg=missing_required_lib('parse'),
            exception=PARSE_ERROR)

    result['strict'] = module.params['strict']
    if len(module.params['matched']) == 0:
        module.fail_json(msg='matched event list param is empty', **result)
    elif len(module.params['dropped']) == 0:
        result['changed'] = True
        result["message"] = "No packet miss"
    else:
        response = get_missing_list(module, result)
        if response:
            result['changed'] = True
        else:
            result['failed'] = True

    module.exit_json(**result)


def main():

    run_module()


if __name__ == '__main__':

    main()
