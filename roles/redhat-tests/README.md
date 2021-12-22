# End to End Tests Suites Role

[Openshift End to End tests](https://github.com/openshift/openshift-tests) are available as a container image in registry.redhat.io/openshift4/ose-tests.

The tests supporte by this role are:
 - [Openshift conformance tests](https://github.com/openshift/openshift-tests)
 - [CSI driver tests](https://redhat-connect.gitbook.io/openshift-badges/badges/container-storage-interface-csi-1/workflow/test-environment) (Badge)

## Variables

The tests executed are defined by the the variable values provided to the role.

Name                               | Default                                    | Description
---------------------------------- | ------------------------------------------ | -------------------------------------------------------------
ts\_e2e\_image                     | quay.io/openshift/origin-tests"            | Image used to execute the tests
ts\_registry                       | registry.dfwt5g.lab:5000                   | Registry used to pull/push images the required images
ts\_registry\_auth                 | auths.json                                 | File with pull secrets for the registries
ts\_ocp\_version\_maj              | 4                                          | OCP version major number, it is recommended to match with the target cluster version
ts\_ocp\_version\_min              | 7                                          | OCP version minor number, it is recommended to match with the target cluster version
ts\_registry\_certificate          | domain.crt                                 | TLS certificate for the registry, if required
ts\_conformance\_tests             | ''                                         | Conformance test to execute
ts\_configs\_dir                   | /home/user/clusterconfigs/                 | Directory that hosts the kubeconfig files and other cluster files that may need to be passed mounted in the test container. This directory will be also used to store the test results.
ts\_csi\_tests\_dir                | /home/user/clusterconfigs/                 | Directory that hosts additional files required during the testing
ts\_csi\_test\_manifest            | ''                                         | Test manifest to be used for the CSI driver tests