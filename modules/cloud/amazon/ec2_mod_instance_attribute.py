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

  source_dest_check:
    description"
      - Modify source_dest_check attribute
    required: false
    default: null
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
    source_dest_check: False

'''

import boto.ec2
from boto.exception import BotoServerError

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

def main():
    attribute_map = {
        'source_dest_check':'sourceDestCheck'
    }

    argument_spec = ec2_argument_spec()

    argument_spec.update(dict(
        instance_ids = dict(type='list', default=[]),
        source_dest_check = dict(type='bool')
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    instance_ids = module.params.get('instance_ids')

    try:
        ec2_conn = ec2_connect(module)
    except BotoServerError as e:
        module.fail_json(msg=e.message)

    results = {}

    changed = False

    for id in instance_ids:
        for param, attr in attribute_map.iteritems():

            val = module.params.get(param)

            if module.params.get(param) != 'None':
                attribute = ec2_conn.get_instance_attribute(instance_id=id, attribute=attr)

                if val == attribute[attr]:
                    continue
            try:
                ec2_conn.modify_instance_attribute(instance_id=id,
                                          attribute=attr, value=val)
                changed = True

                results = {
                    id : {
                        param : val,
                    }
                }

            except BotoServerError as e:
                module.fail_json(msg=e.message)

    module.exit_json(changed=changed, results=results)

if __name__ == '__main__':
    main()
