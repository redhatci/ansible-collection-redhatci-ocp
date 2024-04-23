manage_firewalld_zone
=====================

This role can manage a given firewalld zone and add interfaces to it

Requirements
------------

* `ansible.posix.firewalld` Collection

Role Variables
--------------

| Variable      | Default   | Description                           |
|---------------|-----------|---------------------------------------|
| mfz_zone      |           | Name of the firewalld zone            |
| mfz_state     | present   | State of the firewalld zone           |
| mfz_masquerade| false     | Manage masquerading for the zone      |
| mfz_ifaces    | []        | List of interfaces to add to the zone |
| mfz_services  | {}        | Key/value pairs of service and state  |
| mfz_ports     | {}        | Key/value pairs of ports and state    |


Example Playbook
----------------

```yaml
  - hosts: servers
    gather_hosts: true
    tasks:
      - ansible.builtin.include_role:
          name: redhatci.ocp.manage_firewalld_zone
        vars:
          mfz_zone: restricted  # if the zone doesn't exist it will be created
          mfz_masq: false  # this zone won't forward traffic
          mfz_ifaces:
            - virbr0
            - virbr1
          mfz_services:
            http: true  # allow service
            https: true  # allow service
            ssh: false  # ensure service is rejected
          mfz_ports:
            8080/tcp: true  # open port
            8088/tcp: true  # open port
            8000/tcp: false  # ensure port is closed
```

License
-------

Apache 2.0
