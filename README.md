# Ansible-oss: Sailthru Ansible tools
Collection of Ansible tools developed to manage the Sailthru stacks

# Using
We have a convenient script to load the modules, lookups and tools from our ansible-oss repository:
 * Clone the ansible-oss repo:
   * ``` git clone git@github.com:sailthru/ansible-oss.git ansible-oss```
 * Source the load script to add the modules to ansible's path:
   * ``` source ansible-oss/bin/load.sh ```
 *  Run your playbooks

## Modules 
### Cloud AWS

* cloud/amazon/ec2_instance_status_checks.py
* cloud/amazon/ec2_mod_instance_attribute.py
* cloud/amazon/ec2_ecr_authorization_facts.py

### Cluster
* modules/clustering/zookeeper_exhibitor_facts.py

## Plugins
### with loop plugins

* plugins/lookup_plugins/loops/merge.py

### Clud AWS plugins

* plugins/lookup_plugins/cloud/amazon/ec2_vpc_route_table_helper.py
