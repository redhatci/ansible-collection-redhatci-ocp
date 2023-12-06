# setup_minio role

This role allows the deployment of [Minio](https://min.io/). Minio is a S3 compatible storage provisioner.

Role tasks:
  - Validates requirements
  - Creates a Minio deployment
  - Create a service for the deployment
  - Create an initial S3 bucket

## Variables

| Variable                               | Default                       | Required   | Description                                         |
| -------------------------------------- | ----------------------------- | ---------- | ----------------------------------------------------|
| sm_minio_image                         | quay.io/minio/minio           | No         | Default Minio server image                          |
| sm_minio_client                        | quay.io/minio/mc              | No         | Default Minio client image                          |
| sm_claim_size                          | 10Gi                          | No         | Requested storage for Minio                         |
| sm_storage_class                       | undefined                     | Yes        | A storage Class with Support for RWX volumes        |
| sm_namespace                           | minio                         | No         | Deployment Namespace                                |
| sm_access_key_id                       | minioadmin                    | No         | Minio's Initial Username                            |
| sm_access_key_secret                   | minioadmin                    | No         | Minio's Initial Password                            |
| sm_bucket_name                         | minio                         | No         | Initial Bucket name                                 |
| sm_action                              | install                       | No         | Default role's action                               |
| sm_service_type                        | NodePort                      | No         | Type of service: NodePort, LoadBalacer or ClusterIP |

## Role requirements
  - A storage class with Support for ReadWriteMany volumes. NFS based providers are suitable for this. The PVC bound will fail if RWX mode is not supported.
  - 10Gi available in the defined StorageClass
  - When enabling the service to use a external IP (`sm_service_type: LoadBalacer`) MetalLB operator is required to be installed and configured in the cluster.

## Usage example

See below for some examples of how to use the ocp_logging role to configure the logging subsystem.

Passing the variables at role level:
```yaml
- name: "Setup Minio deployment"
  include_role:
    name: redhatci.ocp.setup_minio
  vars:
    sm_minio_image: quay.io/minio/minio:latest
```

Remove resources created by the role.
```yaml
- name: "Setup OCP logging stack"
  include_role:
    name: redhatci.ocp.setup_minio
    sm_action: cleanup
```

# Access the Minio

See below how to consume the services provided by Minio.

## From other namespaces:
  - http://\<service_name\>.\<namespace\>:9000

## From outside the cluster:

### When using LoadBalacer or NodePort
> NOTE: The variable `sm_service_type: LoadBalacer` is required to enable external access to the service.

Get the external IP assigned and port to the Kubernetes service. In the command shown below is 10.20.30.40:9000
```
$ oc get svc
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
minio-service   LoadBalancer   172.30.108.47   10.20.30.40   9000:31203/TCP   28m
```

Use the endpoint to connect:
  - http://\<external-ip\>:\<port\>

### When using NodePort service type (default)

Get a node IP and the node port assigned to the Kubernetes service. In the command shown below it is 192.168.X.Y and 30521
```
$ oc get nodes -o custom-columns=INTERNAL-IP:status.addresses[0].address

INTERNAL-IP
192.168.X.Y
...

$ oc get svc
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
minio-service   NodePort   172.30.251.192   <none>        9000:30521/TCP   8s
```

Use the endpoint to connect:
  - http://\<node-ip\>:\<node_port\>

# References

* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
* [dci-openshfit-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent/): An agent that allows the deployment of workloads and certification testing on top OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
