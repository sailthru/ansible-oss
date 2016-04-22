# Cloud AWS modules

##### ec2_instance_status_checks
Perform instance System Status and Instance Status checks.
Wait x seconds for the status to be in 'ok' state.
Returns instances that passed and failed the checks.
```
- ec2_instance_status_checks:
    id:
      - i-123456
      - i-654321
    profile: "{{ boto_profile }}"
    region: "{{ region }}"
    wait_timeout: 300
```
```
ok: [localhost] => {
    "msg": {
        "changed": false, 
        "status": {
            "failed": [
                {
                    "id": "i-654321", 
                    "instance_status": "initializing", 
                    "system_status": "initializing"
                }
            ], 
            "passed": [
                {
                    "id": "i-123456", 
                    "instance_status": "ok", 
                    "system_status": "ok"
                }
            ]
        }
    }
}

```
##### ec2_mod_instance_attribute
Modify instance attributes.

```
- ec2_mod_instance_attribute:
    profile: "{{ boto_profile }}"
    region: "{{ region }}"
      instance_ids:
        - i-123456
      attributes: {'sourceDestCheck':'true'}
```
```
changed: [localhost] => {
    "changed": true, 
        "results": {
            "i-123456": 
                { "sourceDestCheck": true }
        }
    }
```
