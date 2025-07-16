# Event structure

Sample event data can be seen here [`event.json`](event.json)

The event contains the following main sections:

## Top Structure Overview

| Attribute coordinate  | Contains |
| --------------------- | ---------------------------------------------------------------------------------- |
| `host`                | Target host for event delivery                                                     |
| `source`              | Source system that generated the event                                             |
| `sourcetype`          | Event format identifier                                                            |
| `event.metadata`      | metadata about ci/cd,runner,pipeline, job source and product                       |
| `event.test`          | Test execution data: results, properties and timings of test suites and test cases |

## Key Components

### Metadata

#### CI Information

Info about the CI - URLs, type

##### Runner

Runner architecture, container technology, executor details

#### Pipeline Information

pipeline info, urls, results and timings

#### Job Information

Job/Build info, URLs, triggers, results and timings

#### Source Information

Author details, repository details

##### Change Information

change/PR information

#### Product Information

product/component/topic/version etc.

### Test Results

- **Summary**: Overall test counts (errors, failures, skipped, total)

#### Test Suites

Grouped test results with properties and individual test cases

For each test suite:

##### Test Cases

Individual test execution details with results, timing, and system output
