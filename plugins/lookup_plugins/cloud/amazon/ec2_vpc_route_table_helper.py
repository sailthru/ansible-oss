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
Description: This lookup takes an AWS region, list of routes and AWS profile
It will lookup the id's for tags of 'instance_id'

Example Usage:

"routes": [
    {
        "dest": "10.1.0.0/0", 
        "instance_id": "nat_instance_name_tag"
    }
]

{{ lookup('ec2_vpc_route_table_helper', ('us-east-1', '{{ routes }}', 'tag:Name' '{{ profile }}')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase
import json
try:
    import boto
    import boto.vpc
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_vpc_id_from_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        self.region = []
        self.routes = []
        self.filter = []
        self.profile = None

    def lookup_ig(self, name):
        if name is None:
            return None

        try:
            vpc_conn = boto.vpc.connect_to_region(region_name=self.region, profile_name=self.profile)
        except Exception as e:
            raise AnsibleError(e)
        filters = {'tag:Name': name}
        gateway = vpc_conn.get_all_internet_gateways(filters=filters)

        if gateway and gateway[0]:
            return gateway[0].id.encode('utf-8')
        return name

    def lookup_instance(self, name):
        try:
            ec2_conn = boto.ec2.connect_to_region(region_name=self.region, profile_name=self.profile)
        except Exception as e:
            raise AnsibleError(e)
        filters = {self.filter: name}

        reservations = ec2_conn.get_all_instances(filters=filters)
        instances = [i for r in reservations for i in r.instances]

        for instance in instances:

            if instance.state == 'terminated' or instance.state == 'stopped':
                continue
            return instance.id.encode('utf-8')

        return name

    def run(self, terms, variables=None, **kwargs):
        self.region = terms[0][0]
        self.routes = terms[0][1]
        self.filter = terms[0][2]

        if len(terms[0]) == 3:
            self.profile = terms[0][3]

        routes = []
        for route in self.routes:
            for key in route:
                if key == 'instance_id':
                    route[key]=self.lookup_instance(route[key])
                if key == 'gateway_id':
                    route[key]=self.lookup_ig(route[key])
            routes.append(route)

        return [str(routes)]