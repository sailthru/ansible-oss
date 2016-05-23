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
##### ec2_ecr_authorization_facts
Retrieves a token that is valid for a specified registry for 12 hours. This command allows you to use the docker CLI to push and pull images with Amazon ECR. If you do not specify a registry, the default registry is assumed.
```
- ec2_ecr_authorization_facts:
    registry_ids: 
      - 123456789123456789
      - 987654321987654321
    region: us-east-1
    profile: boto_dev_profile
```
```
ok: [localhost] => {
    "msg": {
        "changed": false, 
        "results": [
            {
                "endpoint": "https://123456789123456789.dkr.ecr.us-east-1.amazonaws.com", 
                "expires": "2016-05-24T03:42:17.216000-04:00", 
                "registry_id": "123456789123456789", 
                "token": "IyBMaWNlbnNlZCB0byB0aGUgQXBhY2hlIFNvZnR3YXJlIEZvdW5kYXRpb24gKEFTRikgdW5kZXIgb25lDQojIG9yIG1vcmUgY29udHJpYnV0b3IgbGljZW5zZSBhZ3JlZW1lbnRzLiAgU2VlIHRoZSBOT1RJQ0UgZmlsZQ0KIyBkaXN0cmlidXRlZCB3aXRoIHRoaXMgd29yayBmb3IgYWRkaXRpb25hbCBpbmZvcm1hdGlvbg0KIyByZWdhcmRpbmcgY29weXJpZ2h0IG93bmVyc2hpcC4gIFRoZSBBU0YgbGljZW5zZXMgdGhpcyBmaWxlDQojIHRvIHlvdSB1bmRlciB0aGUgQXBhY2hlIExpY2Vuc2UsIFZlcnNpb24gMi4wICh0aGUNCiMgIkxpY2Vuc2UiKTsgeW91IG1heSBub3QgdXNlIHRoaXMgZmlsZSBleGNlcHQgaW4gY29tcGxpYW5jZQ0KIyB3aXRoIHRoZSBMaWNlbnNlLiAgWW91IG1heSBvYnRhaW4gYSBjb3B5IG9mIHRoZSBMaWNlbnNlIGF0DQoNCiMgICBodHRwOi8vd3d3LmFwYWNoZS5vcmcvbGljZW5zZXMvTElDRU5TRS0yLjANCg0KIyBVbmxlc3MgcmVxdWlyZWQgYnkgYXBwbGljYWJsZSBsYXcgb3IgYWdyZWVkIHRvIGluIHdyaXRpbmcsDQojIHNvZnR3YXJlIGRpc3RyaWJ1dGVkIHVuZGVyIHRoZSBMaWNlbnNlIGlzIGRpc3RyaWJ1dGVkIG9uIGFuDQojICJBUyBJUyIgQkFTSVMsIFdJVEhPVVQgV0FSUkFOVElFUyBPUiBDT05ESVRJT05TIE9GIEFOWQ0KIyBLSU5ELCBlaXRoZXIgZXhwcmVzcyBvciBpbXBsaWVkLiAgU2VlIHRoZSBMaWNlbnNlIGZvciB0aGUNCiMgc3BlY2lmaWMgbGFuZ3VhZ2UgZ292ZXJuaW5nIHBlcm1pc3Npb25zIGFuZCBsaW1pdGF0aW9ucw0KIyB1bmRlciB0aGUgTGljZW5zZS4="
            }, 
            {
                "endpoint": "https://987654321987654321.dkr.ecr.us-east-1.amazonaws.com", 
                "expires": "2016-05-24T03:42:17.255000-04:00", 
                "registry_id": "987654321987654321", 
                "token": "SXlCTWFXTmxibk5sWkNCMGJ5QjBhR1VnUVhCaFkyaGxJRk52Wm5SM1lYSmxJRVp2ZFc1a1lYUnBiMjRnS0VGVFJpa2dkVzVrWlhJZ2IyNWxEUW9qSUc5eUlHMXZjbVVnWTI5dWRISnBZblYwYjNJZ2JHbGpaVzV6WlNCaFozSmxaVzFsYm5SekxpQWdVMlZsSUhSb1pTQk9UMVJKUTBVZ1ptbHNaUTBLSXlCa2FYTjBjbWxpZFhSbFpDQjNhWFJvSUhSb2FYTWdkMjl5YXlCbWIzSWdZV1JrYVhScGIyNWhiQ0JwYm1admNtMWhkR2x2YmcwS0l5QnlaV2RoY21ScGJtY2dZMjl3ZVhKcFoyaDBJRzkzYm1WeWMyaHBjQzRnSUZSb1pTQkJVMFlnYkdsalpXNXpaWE1nZEdocGN5Qm1hV3hsRFFvaklIUnZJSGx2ZFNCMWJtUmxjaUIwYUdVZ1FYQmhZMmhsSUV4cFkyVnVjMlVzSUZabGNuTnBiMjRnTWk0d0lDaDBhR1VOQ2lNZ0lreHBZMlZ1YzJVaUtUc2dlVzkxSUcxaGVTQnViM1FnZFhObElIUm9hWE1nWm1sc1pTQmxlR05sY0hRZ2FXNGdZMjl0Y0d4cFlXNWpaUTBLSXlCM2FYUm9JSFJvWlNCTWFXTmxibk5sTGlBZ1dXOTFJRzFoZVNCdlluUmhhVzRnWVNCamIzQjVJRzltSUhSb1pTQk1hV05sYm5ObElHRjBEUW9OQ2lNZ0lDQm9kSFJ3T2k4dmQzZDNMbUZ3WVdOb1pTNXZjbWN2YkdsalpXNXpaWE12VEVsRFJVNVRSUzB5TGpBTkNnMEtJeUJWYm14bGMzTWdjbVZ4ZFdseVpXUWdZbmtnWVhCd2JHbGpZV0pzWlNCc1lYY2diM0lnWVdkeVpXVmtJSFJ2SUdsdUlIZHlhWFJwYm1jc0RRb2pJSE52Wm5SM1lYSmxJR1JwYzNSeWFXSjFkR1ZrSUhWdVpHVnlJSFJvWlNCTWFXTmxibk5sSUdseklHUnBjM1J5YVdKMWRHVmtJRzl1SUdGdURRb2pJQ0pCVXlCSlV5SWdRa0ZUU1ZNc0lGZEpWRWhQVlZRZ1YwRlNVa0ZPVkVsRlV5QlBVaUJEVDA1RVNWUkpUMDVUSUU5R0lFRk9XUTBLSXlCTFNVNUVMQ0JsYVhSb1pYSWdaWGh3Y21WemN5QnZjaUJwYlhCc2FXVmtMaUFnVTJWbElIUm9aU0JNYVdObGJuTmxJR1p2Y2lCMGFHVU5DaU1nYzNCbFkybG1hV01nYkdGdVozVmhaMlVnWjI5MlpYSnVhVzVuSUhCbGNtMXBjM05wYjI1eklHRnVaQ0JzYVcxcGRHRjBhVzl1Y3cwS0l5QjFibVJsY2lCMGFHVWdUR2xqWlc1elpTND0="
            }
        ]
    }
}

```
