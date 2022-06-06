# Pyxis API to submit Preflight certification results for operators

## Fully automated preflight operator certification flow

- DCI runs preflight tests and generates a file with test results for each operator.
- Result file results.json is parsed and submitted to Pyxis API.
- The submission is triggered automatically when `operator.pyxis_operator_identifier` is defined.