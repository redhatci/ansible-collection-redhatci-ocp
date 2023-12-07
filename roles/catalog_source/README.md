# catalog_source role

A Role to deploy an OLM-based CatalogSource

## Parameters
Name             | Required | Default        | Description
-----------------|----------| ---------------|-------------
cs_name          | Yes      |                | Name of the CatalogSource to create
cs_image         | Yes      |                | Catalog Image URL
cs_namespace     | No       | openshift-marketplace  | Namespace where the CatalogSource will be defined
cs_publisher     | No       | Third Party    | CatalogSource publisher
cs_type          | No       | grpc           | CatalogSource type

## Example of usage
```yaml
- name: "Create a CatalogSource"
  ansible.builtin.include_role:
    name: redhatci.ocp.catalog_source
  vars:
    cs_name: "redhat-catalog"
    cs_namespace: "openshift-marketplace"
    cs_image: "registry.redhat.io/redhat/redhat-operator-index:v4.12"
    cs_publisher: "Red Hat"
```

## Authentication

The cluster nodes must have the proper pullsecrets configured in order to be able to pull the catalog image. The tasks will fail if the image cannot be pulled.
