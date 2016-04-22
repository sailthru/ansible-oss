#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
module: ec2_mod_instance_attribute
short description: Modify AWS EC2 instance attributes
description:
  - Modify AWS EC2 instance attributes
  - Instanves must be in running or stopped state

options:
  region:
    description:
      - The AWS region to use
    required: false
    default: null
    aliases: [ 'aws_region', 'ec2_region' ]

  instance_ids:
    description:
      - list of instance ID's to modify
    required: true
    default: []
    aliases: []

  attributes:
    description:
      - Dictionary of attributes you wish to change:
        - instanceType - A valid instance type (m1.small)
        - kernel - Kernel ID (None)
        - ramdisk - Ramdisk ID (None)
        - userData - Base64 encoded String (None)
        - disableApiTermination - Boolean (true)
        - instanceInitiatedShutdownBehavior - stop|terminate
        - blockDeviceMapping - List of strings - ie: ['/dev/sda=false']
        - sourceDestCheck - Boolean (true)
        - groupSet - Set of Security Groups or IDs
        - ebsOptimized - Boolean (false)
        - sriovNetSupport - String - ie: 'simple'

    required: false
    default: {}
    aliases: []

author: "Taras Lipatov tlipatov@sailthru.com"

extends_documentation_fragment:
    - aws
    - ec2
'''

EXAMPLES = '''
# Disable source_dest_check attribute
- ec2_mod_instance_attribute:
    instance_ids: 
      - i-123456
      - i-654321
    region: us-east-1
    profile: boto_dev_profile
    attributes: {'sourceDestCheck':'true'}

'''

import boto.ec2
from boto.exception import BotoServerError

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

def main():
    argument_spec = ec2_argument_spec()

    argument_spec.update(dict(
        instance_ids = dict(type='list', default=[]),
        attributes = dict(type='dict', default={})
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    instance_ids = module.params.get('instance_ids')
    attributes = module.params.get('attributes')

    try:
        ec2_conn = ec2_connect(module)
    except BotoServerError as e:
        module.fail_json(msg=e.message)

    results = {}

    changed = False

    for id in instance_ids:
        for attr, val in attributes.iteritems():

            current_attribute = ec2_conn.get_instance_attribute(instance_id=id, attribute=attr)

            if str(val).lower() == str(current_attribute[attr]).lower():
                continue
            try:
                run = ec2_conn.modify_instance_attribute(instance_id=id,
                                          attribute=attr, value=val)
                changed = True

                results = {
                    id : {
                        attr : val,
                    }
                }

            except BotoServerError as e:
                module.fail_json(msg=e.message)

    module.exit_json(changed=changed, results=results)

if __name__ == '__main__':
    main()
