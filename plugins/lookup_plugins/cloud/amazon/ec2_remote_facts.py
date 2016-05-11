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
Description: This is a lookup wrapper for the ec2_remote_facts module

This lookup takes the following parameters:
    region: AWS region to connect to - default us-east-1

    profile: AWS profile to use - default is None - see AWS profile docs

    return: list of instance properties to return: default is to return all instance properties
        - Return id and state: return=['id','state']

    filters: dict of filters to apply - default None
        - pass extra filters: filters={'tag:Env':'dev'}

Examples
    Lookup a instance name by 'Name' tag:
        {{ lookup('aws_ec2_instance_lookup', filters={'tag:Name':'web-server', 'tag:Env:prod'}, profile=aws_profile) }}

        Returns a list of dictionaries with all instance properties that match the tag:Name 'web-server' and tag:Env 'prod'

    Pass additional lookups: 
        {{ lookup('aws_ec2_instance_lookup', filters={'tag:Name':'web-server'}, profile=aws_profile, return=['id','state','ip_address'] ) }}

        Returns a list of dictionaries with instance ID, STATE, IP_DDRESS that match the tag:Name 'web_servers'
        [ {
            "id": "i-123456"",
            "state": "running",
            "ip_address": "42.37.230.228",
        } ]

    Get the string value of a property:
        {{ lookup('ec2_remote_facts', filters={'tag:Name':'web-server'}, profile=aws_profile)['id'] }}

        Returns a string value that can be passed as a property to modules
        "i-123456"

    No filters will return ALL properties for all instances
        {{ lookup('ec2_remote_facts') }}

    An approach to iterating through results

    - set_fact:
        running_state: "{'instance-state-name':'running'}"
        running_instances: {{ lookup('ec2_remote_facts', filters=running_state, return=['id'] ) }}
      register: running_instances

    - ec2
        # do something with id in {{ item }}
      with_items: "{{ running_instances | map(attribute='id') | list }}"

"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.modules.extras.cloud.amazon import ec2_remote_facts
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import ast
try:
    import boto
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_ec2_instance_lookup lookup cannot be run without boto installed")

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

        conn = boto.ec2.connect_to_region(region_name=region, profile_name=profile)
        instances = conn.get_only_instances(filters=filters)

        results = []
        d={}

        for instance in instances:
            facts = ec2_remote_facts.get_instance_info(instance)
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
