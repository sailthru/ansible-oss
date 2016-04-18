# (c) 2016, SailThru
"""
Description: itterates over a set of dictionary keys and merges from a default dictionary

This lookup takes 3 parameters:
    to data: dict or list to itterate over, use lists to preserve ordering
    from dict: dict to merge form
    keys: list of top level keys to itterate over in the 'to data', omit to itterate over all

Example:
    data:
        to_data:
            'server1':{
                'host_name':'foo'
            },
            'server2':{
                'host_name':'bar'
            }

        from_dict:
            'defaults':{
                'boo':'bez'
            }

    OR
        to_data: [
            'server1':{
                'host_name':'foo'
            },
            'server2':{
                'host_name':'bar'
            }

        from_dict:
            'defaults':{
                'boo':'bez'
            }
        ]


    - debug:
        var: item
      with_mergedict:
      - "{{ to_data }}"
      - "{{ from_dict }}"

      result:
        'item':{
            'host_name':'foo',
            'boo':'bez',
            'mergedict_key':'server1'
        },
        'item':{
            'host_name':'bar',
            'boo':'bez',
            'mergedict_key':'server2'
        }

    - debug:
        var: item
      with_mergedict:
      - "{{ to_data }}"
      - "{{ from_dict }}"
      - ['server2']

      result:
        'item':{
            'host_name':'bar',
            'boo':'bez',
            'mergedict_key':'server2'
        }
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError, AnsibleUndefinedVariable
from ansible.utils.listify import listify_lookup_plugin_terms
import json
from copy import deepcopy

class LookupModule(LookupBase):

    def dict_merge(self, a, b):
        if not isinstance(b, dict):
            return b
        result = deepcopy(a)
        for k, v in b.iteritems():
            if k in result and isinstance(result[k], dict):
                    result[k] = self.dict_merge(result[k], v)
            else:
                # result[k] = deepcopy(v)
                if isinstance(v, list):
                    if k in result and isinstance(result[k], list):
                        result[k] = v + result[k]
                    else:
                        result[k] = deepcopy(v)
                else:
                    result[k] = deepcopy(v)
        return result

    def run(self, terms, variables, **kwargs):
        if len(terms) <= 1:
            raise AnsibleUndefinedVariable("Mergedict takes 2 options")

        if not (isinstance(terms[0], dict) or isinstance(terms[0], list)):
            raise AnsibleUndefinedVariable("First option must be a dict or list")

        if not isinstance(terms[1], dict):
            raise AnsibleUndefinedVariable("Second option must be a dict")

        result=[]
        temp={}

        to_data = terms[0]
        from_dict = terms[1]

        for item in to_data:
            if isinstance(to_data, list):
                temp = self.dict_merge(from_dict.copy(), item)

            if isinstance(to_data, dict):
                if len(terms) == 3:
                    if isinstance(terms[2], list):
                        if item not in terms[2]:
                            continue
                    else:
                       raise AnsibleUndefinedVariable("Third option must be a list")

                temp = self.dict_merge(from_dict.copy(), to_data[item])
                temp['key'] = item

            result.append(temp)

        return result
