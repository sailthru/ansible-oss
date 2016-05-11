#!/usr/bin/env python
#
# (c) 2016, SailThru
# Taras Lipatov <tlipatov@sailthru.com>
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Todo: 
#  add ability to be used as a standalone module
#  add ability to be used as a vars_plugin 

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: echelon
short_desription: hierarchical data lookup
description:
    - resolve data hierarchy with namespaces against multiple backends
    - Returns values by resolving hierarches by merging the results top to bottom
options:
    conf_file:
        description:
            - Hierarchy configuration file
        defautlt: echelon.yml
        required: false
'''

EXAMPLES = '''
# Resolve the hierarchy
- echelon:

# Pass config file
- echelon:
    conf_file: group_vars/echelon/echelon.yml
'''

import os.path
import imp
from copy import deepcopy
from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.plugins.lookup import LookupBase
from jinja2 import Environment, Undefined

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        result = []

        data_dir = kwargs.get('data_dir', 'data')
        conf_file = kwargs.get('conf_file', 'echelon.yml')

        echelon = Echelon(self)
        echelon_data = echelon.run(data_dir=data_dir, conf_file=conf_file)

        jenv = Environment(undefined=SilentUndefined)

        for term in terms:
            lookup = "{{ %s }}" % term
            jtemplate = jenv.from_string(lookup)
            out = jtemplate.render(echelon_data)
            result.append(out)

        return result

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        data_dir = self._task.args.get('data_dir', 'data')
        conf_file = self._task.args.get('conf_file', 'echelon.yml')

        echelon = Echelon(self)

        try:
            result['ansible_facts'] = echelon.run(data_dir=data_dir, conf_file=conf_file)
        except Exception as e:
            result['failed'] = True
            result['msg'] = type(e).__name__ + ": " + str(e)
            
            return result

        return result

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return u''

class Echelon(object):
    def __init__(self, base):
        self.base = base

    def merge_dicts(self, a, b):
        if not isinstance(b, dict):
            return b
        result = deepcopy(a)
        for k, v in b.iteritems():
            if k in result and isinstance(result[k], dict):
                    result[k] = self.merge_dicts(result[k], v)

            else:
                if isinstance(v, list):
                    if k in result and isinstance(result[k], list):
                        result[k] = v + result[k]
                    else:
                        result[k] = deepcopy(v)
                else:
                    result[k] = deepcopy(v)
        return result

    def template_loader(self, ds):
        loaded_yaml = {}
        try:
            loaded_yaml = self.base._templar.template(variable=ds, preserve_trailing_newlines=True, 
                            fail_on_undefined=False, escape_backslashes=False, convert_data=False)
        except Exception as e:
            raise AnsibleError("Unable process template from file (%s): %s " % (ds, str(e)))
            # pass
        return loaded_yaml

    def backend_loader(self,backend=None, conf=None):
        backend_path=os.path.dirname(os.path.realpath(__file__))
        b = imp.load_source('echelon_%s' % backend, '%s/echelon_%s.py' % (backend_path, backend))
        e = b.Backend(conf)
        return e

    def run(self, data_dir='data', conf_file='echelon.yml'):
        from ansible.parsing.dataloader import DataLoader

        loader = DataLoader()
        ds = loader.load_from_file(conf_file)
        conf_data=self.template_loader(ds) 

        hierarchies={}
        if not 'hierarchy' in conf_data:
            return hierarchies

        # Load the backends
        backends={}
        if not 'backends' in conf_data:
            raise AnsibleError("No 'backends' found in echeclon config file")

        backend_plugins = []
        for backend in conf_data['backends']:
            for k in backend:
                try:
                    backend_plugins.append(self.backend_loader(k,backend[k]))
                except Exception as e:
                    raise AnsibleError("Failed to load backend plugin (%s): %s" % (k, str(e)))

        for hierarchy in conf_data['hierarchy']:
            for k in hierarchy:
                data = {}
                for path in hierarchy[k]:
                    for plugin in backend_plugins:
                        full_path = "%s/%s" % (k,path)
                        data_new = self.template_loader(plugin.main(full_path))
                        if data_new == {}:
                            continue
                        else:
                            data = self.merge_dicts(data_new, data)
                            break
                    hierarchies[k] = data

        return hierarchies

def main():
    results = {}
    return results

if __name__ == '__main__':
    main()   
