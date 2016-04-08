#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
module: ec2_instance_status_checks
short description: Perform instance status checks  with wait option
description:
    - Perform instance status checks
    - Wait for x seconds for the status to be in 'ok' state
    - Check for system status and / or instance status
    - Returns list of instances that passed and failed the checks

options:
  id:
    description:
      - list of instance ID's to check
    required: True
  wait_timeout:
    description:
      - Amount of seconds to wait for instance status to chage to 'ok' state
    required: False
    default: 0
  system_status:
    description:
      - Perform system_status check
    required: False
    default: True
  instance_status:
    description:
      - Perform instance_status check
    required: False
    default: True
  fail:
    description:
      - Fail if any instances checks did not pass
    required: False
    default: False

author: "Taras Lipatov tlipatov@sailthru.com"
extends_documentation_fragment:
    - aws
    - ec2

'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.

# Get instance status
- ec2_instance_status_check
    id:
      - i-123456

# Wait for both instnce checks to be in 'ok' state for 300 seconds
- ec2_instance_status_check
    id:
      - i-123456
    wait_timeout: 300

# Wait 300 seconds for system status check to be in 'ok' state and fail if it is not
# after the wait_timeout is exceeded
- ec2_instance_status_check
    id:
      - i-123456
    wait_timeout: 300
    instance_status: False
    system_status: True
    fail: True

'''

import boto.ec2
from boto.exception import BotoServerError

# import json
import time

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

def get_status(instance):

    status = {}
    system_status = instance.system_status.status
    instance_status  = instance.instance_status.status
    instance_id = instance.id

    status =  { 
        'id': instance_id,
        'instance_status': instance_status,
        'system_status': system_status
        }

    return status

def main():

    argument_spec = ec2_argument_spec()

    argument_spec.update(dict(
            id = dict(type='list', default=[]),
            wait_timeout = dict(type='int', default=0),
            system_status = dict(type='bool', default=True),
            instance_status = dict(type='bool', default=True),
            fail = dict(type='bool', default=False)
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    id = module.params.get('id')
    wait_timeout = module.params.get('wait_timeout')
    filters = module.params.get("filters")
    system_status_check = module.params.get("system_status")

    instance_status_check = module.params.get("instance_status")
    fail = module.params.get("fail")

    try:
        ec2_conn = ec2_connect(module)
    except BotoServerError as e:
        module.fail_json(msg=e.message)

    status = {}
    status['passed'] = []
    status['failed'] = []

    timeout = time.time() + wait_timeout

    while True:
        if len(id) == 0:
            break

        try:
            instances = ec2_conn.get_all_instance_status(instance_ids=id, filters=filters)
        except BotoServerError as e:
            module.fail_json(msg=e.message)

        for i in instances[:]:

            instance_status = get_status(i)

            if system_status_check and instance_status_check:
                if instance_status['system_status'] == 'ok' and instance_status['instance_status'] == 'ok':
                    status['passed'].append(instance_status)
                    id.remove(i.id)
                    instances.remove(i)

            if system_status_check and not instance_status_check:
                if instance_status['system_status'] == 'ok':
                    status['passed'].append(instance_status)
                    id.remove(i.id)
                    instances.remove(i)

            if not system_status_check and instance_status_check:
                if instance_status['instance_status'] == 'ok':
                    status['passed'].append(instance_status)
                    id.remove(i.id)
                    instances.remove(i)

        # test = 0
            if time.time() >= timeout:
                break
        # test = test - 1
        # Sleep for 1 second so we dont hammer the AWS API
        time.sleep(1)

    for i in instances[:]:
        instance_status = get_status(i)
        status['failed'].append(instance_status)


    if len(instances) > 0 and fail is True:
        module.fail_json(msg="Timeout when waiting for instance status checks", status=status)
    else:
        module.exit_json(status=status)

if __name__ == '__main__':
    main()