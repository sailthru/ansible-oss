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
module: ec2_ecr_authorization_facts
short description: Retreive Amazon EC2 ECR uthorization Facts
description:
  - Retreive Amazon EC2 ECR uthorization Facts

options:
  region:
    description:
      - The AWS region to use
    required: false
    default: null
    aliases: [ 'aws_region', 'ec2_region' ]

  registry_ids:
    description:
      - list of registry ID's to get uthorization facts for
    required: true
    default: []
    aliases: []

author: "Taras Lipatov tlipatov@sailthru.com"

extends_documentation_fragment:
    - aws
    - ec2
'''

EXAMPLES = '''
# Get ECR uthorization facts
- ec2_ecr_authorization_facts:
    registry_ids: 
      - 123456789123456789
      - 987654321987654321
    region: us-east-1
    profile: boto_dev_profile

'''
try:
    import boto3
    import botocore.exceptions.ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

def main():
    argument_spec = ec2_argument_spec()

    argument_spec.update(dict(
        registry_ids = dict(type='list', default=[])
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    registry_ids = module.params.get('registry_ids')
    results = []

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    try:
        region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        if not region:
            module.fail_json(msg="Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file")
        ecr = boto3_conn(module, conn_type='client', resource='ecr', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound, e:
        module.fail_json(msg="Can't authorize connection - "+str(e))

    for id in registry_ids:
        try:
            response = ecr.get_authorization_token(
                registryIds = [id]
            )
        except Exception, e:
            module.fail_json(msg="Can't get authorization token  - "+str(e))


        results.append( {
            'registry_id' : id,
            'token' : response["authorizationData"][0]["authorizationToken"],
            'endpoint' : response["authorizationData"][0]["proxyEndpoint"],
            'expires' : response["authorizationData"][0]["expiresAt"]
        } )

    module.exit_json(results=results)

if __name__ == '__main__':
    main()