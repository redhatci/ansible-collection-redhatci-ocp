# Verify JUnit tests Role

This role takes a list of expected results per filename and verifies their
_inclusion_ into a list of actual results.

For example, you could provide just two tests to verify against a JUnit file with hundreds of tests. If these expected tests are in the list of the actual results, the job will pass. If they're absent, or the results for them differ from the expected, the job will fail.

Name                  | Default      | Description
--------------------- | ------------ | -------------
tests_to_verify       | undefined    | There is a complex list of expected results, where each element contains a JUnit filename (supports globbing) and a corresponding list of expected results. A sublist of expected results could include one or more pairs of 'testcase name' and 'passed'/'failed'.
skip_absent_testfiles | false        | Use this option to prevent the verification process from failing if the JUnit file listed in the expected results is not present.
junit_fix_tags        | false        | Please use this option to add the missing <testsuites></testsuites> tags to the JUnit file in order to fix the formatting.

```yaml
# Example of the list of expected results per file (supports globbing).
# expected_results/testcase could contain Python regex.
# Please use single quotes with regex to avoid Python/Ansible syntax interference.
tests_to_verify:
  - filename: "preflight_container_simple-demo-operator_0.0.6_kube-rbac-proxy_results-junit.xml"
    expected_results:
      - testcase: 'Has\w+Tag'
        passed: True
      - testcase: 'LayerCountAcceptable'
        passed: True
      - testcase: 'RunAsNonRoot'
        passed: True
  - filename: "preflight_container_simple-demo-operator_0.0.6_simple-demo-operator_*_results-junit.xml"
    expected_results:
      - testcase: '[a-zA-Z]+'
        passed: True
      - testcase: 'HasUniqueTag'
        passed: True
      - testcase: 'Has*'
        passed: True
      - testcase: 'Run[a-zA-Z]{5}Root'
        passed: True
      - testcase: 'BasedOnUbi'
        passed: True
  - filename: "preflight_operator_simple-demo-operator_0.0.6_results-junit.xml"
    expected_results:
      - testcase: '[a-zA-Z0-9]+'
        passed: True
```
