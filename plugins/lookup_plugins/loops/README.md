# Loop plugins

##### mergedict.py
Itterates over a set of dictionary keys and merges from a default dictionary
```
servers:
    'server1':{
        'host_name':'foo'
    },
    'server2':{
        'host_name':'bar'
    }

defaults:
    'defaults':{
        'boo':'bez'
    }
```
```
- debug:
    msg: "{{ item }}"
    with_mergedict:
      - "{{ servers }}"
      - "{{ defaults }}"
```
```
result:
    'item':{
        'host_name':'foo',
        'boo':'bez',
        'key':'server1'
    },
    'item':{
        'host_name':'bar',
        'boo':'bez',
        'key':'server2'
    }
```