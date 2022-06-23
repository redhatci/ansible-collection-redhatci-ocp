# Verify JUnit tests Role

This role takes a list of expected results per filename and verifies their
_inclusion_ into a list of actual results.

For example, you could provide just two tests to verify against a JUnit file with hundreds of tests. If these expected tests are in the list of the actual results, the job will pass. If they're absent, or the results for them differ from the expected, the job will fail.


Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
tests\_to\_verify               | undefined                                                | A complex list of expected results. Each element contains a JUnit filename and a list of expected resuls for that filename. A sublist of expected results could contain one or more pair "testcase name"-"passed".

```yaml
# example of the list of expected results per file
tests_to_verify:
  - filename: "preflight_container_simple-demo-operator_0.0.6_kube-rbac-proxy_results-junit.xml"
    expected_results:
      - testcase: HasUniqueTag
        passed: False
      - testcase: LayerCountAcceptable
        passed: True
  - filename: "preflight_container_simple-demo-operator_0.0.6_simple-demo-operator_results-junit.xml"
    expected_results:
      - testcase: HasLicense
        passed: True
      - testcase: HasUniqueTag
        passed: True
      - testcase: LayerCountAcceptable
        passed: True
      - testcase: HasNoProhibitedPackages
```
