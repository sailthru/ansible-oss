# Cluster modules

##### zookeeper_exhibitor_facts
Retrieve Zookeeper exhibitor statu

```
- zookeeper_exhibitor_facts:
    exhibitor_url: 'http://localhost:8080'
  register: zookeeper_exhibitor_facts

```
```
ok: [localhost] => {
    "msg": {
        "changed": false, 
        "results": {
            "instances": [
                {
                    "172.24.9.11": {
                        "errorMessage": "", 
                        "response": {
                            "description": "serving", 
                            "isLeader": true, 
                            "state": 3, 
                            "switches": {
                                "backups": true, 
                                "cleanup": true, 
                                "restarts": true
                            }
                        }, 
                        "success": true
                    }
                }, 
                {
                    "172.24.8.12": {
                        "errorMessage": "", 
                        "response": {
                            "description": "serving", 
                            "isLeader": false, 
                            "state": 3, 
                            "switches": {
                                "backups": true, 
                                "cleanup": true, 
                                "restarts": true
                            }
                        }, 
                        "success": true
                    }
                }, 
                {
                    "172.24.7.13": {
                        "errorMessage": "", 
                        "response": {
                            "description": "serving", 
                            "isLeader": false, 
                            "state": 3, 
                            "switches": {
                                "backups": true, 
                                "cleanup": true, 
                                "restarts": true
                            }
                        }, 
                        "success": true
                    }
                }
            ], 
            "status": [
                {
                    "code": 3, 
                    "description": "serving", 
                    "hostname": "172.24.9.11", 
                    "isLeader": true
                }, 
                {
                    "code": 3, 
                    "description": "serving", 
                    "hostname": "172.24.8.12", 
                    "isLeader": false
                }, 
                {
                    "code": 3, 
                    "description": "serving", 
                    "hostname": "172.24.7.13", 
                    "isLeader": false
                }
            ]
        }
    }
}
```