# HostPath Storage Role

Role to setup HostPath storage provisioner using KubeVirt. A HostPathProvisioner object from the kubevirt.io group is created along with a storage class named managed-hostpath-storage and set as default if no other default Storage Class is defined.

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|--------------------------------------
hps_path                    | No        | /var/hostpath-provisioner | Host path where persistent volumes will be created
hps_storage_pool            | No        | hostpath-pool          | Name of the storage pool for the HostPathProvisioner
hps_namespace               | No        | openshift-hostpath-storage | Deployment namespace
hps_node_selector           | No        | {}                     | Node selector for HostPathProvisioner placement
hps_storage_class_name      | No        | managed-hostpath-storage | Name of the storage class to create

### Requirements

* KubeVirt and CDI operators installed on the cluster
* Nodes with sufficient local storage space at the specified host path
* Proper permissions for the HostPath directory on target nodes

## Example of usage

### Basic usage with defaults
```yaml
- name: "Setup HostPath Storage Provisioner with defaults"
  ansible.builtin.include_role:
    name: redhatci.ocp.acm.hostpath_storage
```

### Customized usage
```yaml
- name: "Setup HostPath Storage Provisioner with custom settings"
  ansible.builtin.include_role:
    name: redhatci.ocp.acm.hostpath_storage
  vars:
    hps_path: "/mnt/custom-storage"
    hps_storage_pool: "local-storage"
    hps_node_selector:
      kubernetes.io/os: linux
      storage: "true"
```

### Sample manifest to create a persistent volume claim
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: test-hostpath-claim
  annotations:
    volume.beta.kubernetes.io/storage-class: "managed-hostpath-storage"
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: "managed-hostpath-storage"
```

### Sample manifest to create a pod binding to the PVC
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: test-hostpath-pod
spec:
  containers:
  - name: test-pod
    image: registry.access.redhat.com/ubi8/ubi:latest
    command:
      - "/bin/sh"
    args:
      - "-c"
      - "touch /mnt/SUCCESS && sleep 3600"
    volumeMounts:
      - name: hostpath-pvc
        mountPath: "/mnt"
  restartPolicy: "Never"
  volumes:
    - name: hostpath-pvc
      persistentVolumeClaim:
        claimName: test-hostpath-claim
```

## References

* [KubeVirt HostPath Provisioner](https://github.com/kubevirt/hostpath-provisioner)
* [KubeVirt Storage Documentation](https://kubevirt.io/user-guide/storage/)

## License
Apache License, Version 2.0 