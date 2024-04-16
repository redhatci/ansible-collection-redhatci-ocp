# jenkins_job_launcher

jenkins_job_launcher role triggers Jenkins job using the uri module.
This role uses username + user API token to authenticate with Jenkins.

Role Variables
--------------

Name                                | Default   | Required                    | Description
----------------------------------- |-----------|-----------------------------| -------------------------------------------------------------
jjl_job_url                         | undefined | true                        | Jenkins job url.
jjl_job_params                      | undefined | true                        | job params and values based on the playbook example.
jjl_username                        | undefined | true                        | Jenkins user.
jjl_token                           | undefined | true                        | user API token.
          
Example Playbook
----------------

```
  hosts: all
  tasks: 
  - name: trigger jenkins job
    ansible.builtin.import_role: 
      redhatci.ocp.jenkins_job_launcher 
    vars:
      jjl_job_params: "<param>>=<value>&\
                      <param2>=<value>&\"
      jjl_job_url: "https://auto-jenkins-csb-kniqe.apps.ocp-c1.prod.psi.redhat.com/job/ocp-far-edge-vran-deployment"
      jjl_username: <user>
      jjl_token: <token>
```
