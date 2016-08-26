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

"""
Description: This is a lookup wrapper for the ec2_vpc_subnet_facts module

This lookup takes the following parameters:
    region: AWS region to connect to - default us-east-1

    profile: AWS profile to use - default is None - see AWS profile docs

    return: list of vpc subnet properties to return: default is to return all vpc subnet properties
        - Return id and state: return=['vpc_id','state']

    filters: dict of filters to apply - default None
        - pass filters: filters={'tag:Name':'myvpc'}

Examples
    Lookup a subnet name by 'Name' tag:
        {{ lookup('aws_ec2_subnet_lookup', filters={'tag:Name':'myvpc', 'tag:Env:prod'}, profile=aws_profile) }}

        Returns a list of dictionaries with all vpc submets that match the tag:Name 'web-server' and tag:Env 'prod'

    Pass additional lookups: 
        {{ lookup('aws_ec2_subnet_lookup', filters={'tag:Name':'myvpc'}, profile=aws_profile, return=['vpc_id','state'] ) }}

        Returns a list of dictionaries with vpc subnet ID, STATE, IP_DDRESS that match the tag:Name 'myvpc'
        [ {
            "state": "available", 
            "vpc_id": "vpc-1fd99c78
        } ]

    Get the string value of a property:
        {{ lookup('ec2_vpc_subnet_facts', filters={'tag:Name':'myvpc'}, profile=aws_profile)['vpc_id'] }}

        Returns a string value that can be passed as a property to modules
        "vpc-123456"

    No filters will return ALL properties for all vpc submets
        {{ lookup('ec2_vpc_subnet_facts') }}

"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.modules.extras.cloud.amazon import ec2_vpc_subnet_facts
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import ast
try:
    import boto
    import boto.vpc
except ImportError:
    raise AnsibleError("aws_ec2_subnet_lookup lookup cannot be run without boto installed")

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        filters = kwargs.get('filters', None)
        profile = kwargs.get('profile', None)
        return_facts = kwargs.get('return', None)
        region = kwargs.get('region', 'us-east-1')

        if type(return_facts) is str:
            return_facts = return_facts.split(',')
        try:
            connection = boto.vpc.connect_to_region(region_name=region, profile_name=profile)
        except BotoServerError as e:
            raise AnsibleError(e)

        try:
            all_subnets = connection.get_all_subnets(filters=filters)
        except BotoServerError as e:
            raise AnsibleError(e)

        results = []
        d={}

        for subnet in all_subnets:
            facts = ec2_vpc_subnet_facts.get_subnet_info(subnet)
            if return_facts is None:
                results.append(facts)
            else:
                for f in return_facts:
                    try:
                        return_fact = facts[f]
                    except KeyError:
                        return_fact = None
                    d[f]=return_fact
                results.append(d.copy())

        return(results)