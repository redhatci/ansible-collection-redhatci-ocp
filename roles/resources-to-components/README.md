# Resources to components role

This role should be used from `dci-openshift-app-agent` to create DCI components based on Kubernetes resources that are running on the cluster, typically with cases where these resources were created prior to running `dci-openshift-app-agent`, or with resources created during agent's execution.

This role is called in an intermediate step between the install and tests stages, called post-install, to ensure that it creates the components related to the workloads deployed till the install stage, also including workloads that may have been deployed beforehand.

The list of supported resources by this role are listed under the `rtc_supported_resources` variable. The resources in the namespaces with the attribute `metadata.ownerReferences` are skipped. So only non-dependant resources are converted to components.

In particular, this role extracts the container images used in the resources deployed in the selected namespaces. This is the main information used to build the component, as this is the real information that does not change between different jobs if using the same image for the resource (e.g. pod names can change if they are under a deployment, for example).

## Requirements

- This role should be used from `dci-openshift-app-agent`.
- You need to set up `rtc_resources_to_components` variable with the resources to check and the namespace where this role will look at.
- You have to make sure that `rtc_resources_to_components` is defined according to the resources you have deployed in your cluster; else, the role will not autodiscover anything and no components will be created.

## Variables

Name                                    | Default                                                                      | Description
--------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------
rtc\_resources\_to\_components          | []                                                                           | List of Kubernetes resources to be transformed to components. See the example below to check how to build this list.
rtc\_supported\_resources               | ["Pod", "Deployment", "ReplicaSet", "StatefulSet", "ClusterServiceVersion"]  | Resources that can be used to create components based on the container images used on them.

## Example of rtc_resources_to_components

Each entry of this list intends to gather all the resources specified on `resource` field (must be a valid Kubernetes resource, such as `Pod`, for example) in the namespace specified in `namespace` field.

```yaml
---
rtc_resources_to_components:
  - resource: Pod
    namespace: test-cnf
  - resource: ReplicaSet
    namespace: test-cnf
  - resource: Deployment
    namespace: test-cnf
  - resource: ClusterServiceVersion
    namespace: test-cnf
  - resource: Pod
    namespace: production-cnf
  - resource: StatefulSet
    namespace: production-cnf
...
```

With this configuration, this role will check all these resources in `test-cnf` and `production-cnf` namespaces, and will create a DCI component in the OCP topic where the job is launched for each container image extracted.

## Component structure

Naming convention followed for the components created is the following: `IMG <container_image_name> <container_image_version>`, where:

- `IMG`: prefix for placing all the components created on this role in the same position in the component list of the job, just for making readability easier.
- `<container_image_name>`: takes the name of the container image in use.
- `<container_image_version>`: uses the image tag or the digest, depending on what is used.

Regarding the component fields:

- Component name will be the image version, being either image tag (`latest` if ommited) or digest.
- Component type will be the image name, so that we can use that name to retrieve the different components related to the same image name but changing the version (i.e. component name).
- The component canonical project name is formed with the following structure: `IMG <container_image_name> <container_image_version>`.

## License

Apache License, Version 2.0 (see [LICENSE](../../LICENSE) file)
