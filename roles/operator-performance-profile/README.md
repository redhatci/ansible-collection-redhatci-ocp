# Performance profile

The `operator-performance-profile` role configures and deploys the [performance-addon-operator](https://github.com/openshift-kni/performance-addon-operators/blob/master/docs/performance_profile.md) via the [Operator Lifecycle Manager (OLM)](https://olm.operatorframework.io/).
The performance addon operator is installed under the namespace: `openshift-performance-addon-operator`.

## Configuration

Settings that can be used to configure the role:

| Setting                | Required | Type   | Description                          |
| ---------------------- | -------- | ------ | -------------------------------------|
| performance_definition | False    | String | Performance addon config file to use |

Use a custom config file by defining `performance_definition`. When undefined a default configuration based on the OCP version is used. (_See [files](files) directory_ )
