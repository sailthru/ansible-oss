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
module: zookeeper_exhibitor_facts
short description: Retrieve Zookeeper exhibitor status
description:
  - Retrieve Zookeeper exhibitor status

option:
  exhibitor_url:
    description:
      - Zookeeper exhibitor url
    required: True 
    default: 'http://localhost:8080'

author: "Taras Lipatov tlipatov@sailthru.com"
'''

EXAMPLES = '''
- zookeeper_exhibitor_facts:
    exhibitor_url: 'http://localhost:8080'
  register: zookeeper_exhibitor_facts
'''

from ansible.module_utils.basic import *

try:
    import requests
except ImportError:
    requests_found = False
else:
    requests_found = True


def main():
    results = {}
    results['instances'] = []

    module = AnsibleModule(
        argument_spec = dict(
            exhibitor_url = dict(type='str', default='http://localhost:8080'),
        )
    )

    exhibitor_url = module.params.get('exhibitor_url')

    if not requests_found:
        module.fail_json(msg="the python requests library is required")

    api_cluster_v1 = {
        'status' : 'exhibitor/v1/cluster/status',
        'remoteGetStatus' : 'exhibitor/v1/cluster/state'
    }

    url = '%s/%s' % ( exhibitor_url, api_cluster_v1['status'] )
    r = requests.get( url, headers={'Accept': 'application/json'}, timeout=20.0 )

    if r.status_code == 200:
        results['status'] = r.json()

        for host in r.json():
            url = '%s/%s/%s' % ( exhibitor_url, api_cluster_v1['remoteGetStatus'], host['hostname'] )
            r = requests.get( url, headers={'Accept': 'application/json'}, timeout=20.0 )

            instance = {
                host['hostname'] : r.json()
            }

            results['instances'].append( instance )

    module.exit_json(results=results)

if __name__ == '__main__':
    main()