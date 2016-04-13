# Echelon
Echelon is a hierarchical key/value data resolver and lookup for Ansible.

#### Configuration
By default echelon looks for _echelon.yml_ file at the top of the playbook directory. This can be overwritten with the _conf_file_ parameter.

The configuration file consists of two sections.
* hierarchy: a list of hierarchies and paths to resolve
* backends: list of backend data lookup plugins

```
hierarchy:
  - aws:
    - "{{ env }}_ec2"
    - "defaults"
  - app:
    - "{{ env }}_db"
    - "defaults"
backends:
  - yml:
      data_dir: group_vars/echelon/data
```

#### Hierarchy structure
Based on the sample configuration file above, our sample data will look like:
``` 
group_vars/echelon/data/instance_data/prod_ec2.yml

---
ami_id: id-123456
```

``` 
group_vars/echelon/data/instance_data/dev_ec2.yml

---
ami_id: id-789123
```

``` 
group_vars/echelon/data/instance_data/defaults.yml
 
---
security_group: ssh
``` 

```
group_vars/echelon/data/app_data/prod_db.yml
 
---
db_user: prod_user
```

``` 
group_vars/echelon/data/app_data/dev_db.yml

---
db_user: dev_user
```

``` 
group_vars/echelon/data/app_data/default.yml

---
db_user: ops
schema: my_app
```

#### Using Echelon
##### As an action_plugin
Using Echelon as an action_plugin makes all the key/values in the hierarchy availalbe to the play.
Place _echelon.py_ and the backend _echelon_yml.py_ in to your _action_plugins_ dir or point the Ansible ANSIBLE_ACTION_PLUGINS environment varaiable at it
```
# test.yml play book
---
  tasks:
    - echelon:
    
    - debug:
        msg: "{{ aws }}"
    - debug:
        msg: "{{ app }}"
```

```
ansible-playbook test.yml --extra-vars "env=prod"
```
```
ok: [localhost] => {
    "msg": {
       "ami_id": "id-123456",
       "security_group": "ssh"
    }
ok: [localhost] => {
    "msg": {
       "db_user": "prod_user",
       "schema": "my_app"
    }
```

##### As a lookup
Using Echlon as a lookup fetches a single key/value form the hierarchy
Place _echelon.py_ and the backend _echelon_yml.py_ in to your _lookuop_plugins_ dir or point the Ansible ANSIBLE_LOOKUP_PLUGINS environment varaiable at it
```
# test.yml play book
---
  tasks:
    - debug:
        msg: "{{ lookup ( 'echelon', 'aws.ami_id' ) }}"
    - debug:
        msg: "{{ lookup ( 'echelon', 'app.db_user' ) }}"
```
```
ansible-playbook test.yml --extra-vars "env=dev"
```
```
ok: [localhost] => {
    "msg": "id-789123"
}
ok: [localhost] => {
    "msg": "dev_user"
}
```
