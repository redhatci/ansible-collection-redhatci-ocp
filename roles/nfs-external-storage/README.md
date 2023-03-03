# NFS external storage role

Role to NFS external storage provisioner. A storage class named managed-nfs-storage is created and set as default if no other default Storage Class is defined.

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|--------------------------------------
nes_nfs_server              | Yes       | undefined              | NFS server's FQDN or IP Address
nes_nfs_path                | Yes       | undefined              | NFS export path
nes_namespace               | No        | openshift-nfs-storage  | Deployment namespace
nes_provisioner_image       | No        | registry.k8s.io/sig-storage/nfs-subdir-external-provisioner:v4.0.2 | Provisioner image

### Requirements

* A NFS server reachable from the OCP cluster. For details about the proper setup using RHEL see [Installing NFS](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_file_systems/exporting-nfs-shares_managing-file-systems#installing-nfs_exporting-nfs-shares).
* An exported filesystem with the permission according to the pods needs.

## Example of usage

```yaml
- name: "deploy-operators : Install OCS Operator"
  include_role:
    name: nfs-external-storage
  vars:
    nes_nfs_server: "192.168.16.11"
    nes_nfs_path: "/exports/nfs-provisioner"
```

### Sample manifest to create a persistent volume claim
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: test-claim
  annotations:
    volume.beta.kubernetes.io/storage-class: "managed-nfs-storage"
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Mi
```

### Sample manifest to create a pod binding to the PVC
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: test-pod
spec:
  containers:
  - name: test-pod
    image: gcr.io/google_containers/busybox:1.36
    command:
      - "/bin/sh"
    args:
      - "-c"
      - "touch /mnt/SUCCESS && exit 0 || exit 1"
    volumeMounts:
      - name: nfs-pvc
        mountPath: "/mnt"
  restartPolicy: "Never"
  volumes:
    - name: nfs-pvc
      persistentVolumeClaim:
        claimName: test-claim
```

## References

* [External Storage](https://github.com/kubernetes-retired/external-storage/tree/master/nfs-client).
* [Create a storage class for NFS dynamic storage provisioning in an OpenShift environment](https://www.ibm.com/support/pages/how-do-i-create-storage-class-nfs-dynamic-storage-provisioning-openshift-environment).

## License
Apache License, Version 2.0