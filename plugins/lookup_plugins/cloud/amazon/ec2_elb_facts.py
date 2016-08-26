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
Description: This is a lookup wrapper for the ec2_elb_facts module

This lookup takes the following parameters:
    region: AWS region to connect to - default us-east-1

    profile: AWS profile to use - default is None - see AWS profile docs

    return: list of elb properties to return: default is to return all instance properties
        - Return id and state: return=['dns_name']

    filters: List of ELB names to gather facts about. 
             Pass this option to gather facts about a set of ELBs, otherwise, all ELBs are returned.
        - pass extra filters: filters=['elb1':'elb2']

Examples
    Lookup a elb name by 'mame':
        {{ lookup('ec2_elb_facts', filters=['elb1'], profile=aws_profile) }}

        Returns a list of dictionaries with all elb properties that match the elb name 'elb1'

    Pass additional lookups:
        {{ lookup('ec2_elb_facts', filters=['elb1'], profile=aws_profile, return=['dns_name'] ) }}

        Returns a list of dictionaries with elb DNS_NAME
        [ {
            "dns_name": "dev-vpc-myvpc-12345654321.us-east-1.elb.amazonaws.com",
        } ]

    Get the string value of a property:
        {{ lookup('ec2_remote_facts', filters={'tag:Name':'web-server'}, profile=aws_profile)['id'] }}

        Returns a string value that can be passed as a property to modules
        "i-123456"
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.modules.extras.cloud.amazon import ec2_elb_facts
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import ast
try:
    import boto
    # import boto.ec2
    import boto.ec2.elb
except ImportError:
    raise AnsibleError("ec2_elb_facts lookup cannot be run without boto installed")

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        elb_names = kwargs.get('filters', None)
        profile = kwargs.get('profile', None)
        return_facts = kwargs.get('return', None)
        region = kwargs.get('region', 'us-east-1')

        if not elb_names:
            elb_names = None

        connection = boto.ec2.elb.connect_to_region(region_name=region, profile_name=profile)

        try:
            all_elbs = connection.get_all_load_balancers(elb_names)
        except BotoServerError as e:
            return_fact = None

        results = []
        d={}
        for elb in all_elbs:
            facts = ec2_elb_facts.get_elb_info(connection,elb)
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

        return([results])
