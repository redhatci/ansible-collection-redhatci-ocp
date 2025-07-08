# Test Report Send Role - Comprehensive Guide

## Table of Contents

1. [Overview](#overview)
2. [Event Structure](#event-structure)
3. [Metadata Structure](#metadata-structure)
4. [CI System Integration](#ci-system-integration)
   - [Jenkins Integration](#jenkins-integration)
   - [DCI Integration](#dci-integration)
   - [Environment Variable Mapping](#environment-variable-mapping)
5. [Reporting Systems](#reporting-systems)
   - [Splunk Integration](#splunk-integration)
6. [Implementation Guide](#implementation-guide)

---

## Overview

The `test_report_send` role generates events from CI metadata and test reports, then sends these events to reporting systems for observability and analytics. This enables:

- **Shared visual and data languages** across teams and systems
- **Data-based decision-making processes** with comprehensive test and CI insights
- **Cross-CI system compatibility** with normalized event structures

### Key Features

- **Multi-CI Support**: Works with Jenkins, DCI, GitHub, GitLab, and Prow
- **Standardized Events**: Converts diverse CI metadata into unified event structure
- **Test Report Integration**: Processes JUnit format test reports
- **Flexible Reporting**: Supports multiple reporting backends (Splunk, etc.)

---

## Event Structure

Events contain two main components: **metadata** (CI/CD information) and **test data** (test execution results).

### Protocol Buffer Schema Definition

The event structure is formally defined using Protocol Buffers for precise typing and validation:

```protobuf
message TestReportEvent {
    ReportMetadata metadata = 3;        // CI/CD and environment metadata
    TestReport test = 4;                // Test execution data
}

message TestReportPayload {
    string host = 1;                    // Host/container/service identifier
    string sourcetype = 2;              // Event format identifier  
    TestReportEvent event = 3;          // Event container
    optional string source = 4;         // Information source (team/channel)
    optional string _time = 5;          // Event emission timestamp
}
```

### Top-Level Event Structure (JSON Representation)

```json
{
    "source": "<str>",           // Information source (team/channel identifier)
    "host": "<hostname>",        // Host/container/service sending the data
    "sourcetype": "_json",       // Event format identifier
    "_time": "<timestamp>",      // Event emission timestamp
    "event": {
        "metadata": "<metadata_object>",  // CI/CD and environment metadata
        "test": "<test_data_object>"      // Test execution data
    }
}
```

### Key Components

| Component         | Type/Message      | Description                                                   |
| ----------------- | ----------------- | ------------------------------------------------------------- |
| `host`            | `string`          | Target host for event delivery                                |
| `source`          | `string`          | Source system that generated the event                        |
| `sourcetype`      | `string`          | Event format identifier                                       |
| `_time`           | `string`          | Event ingestion timestamp (set by the reporting system)       |
| `event`           | `TestReportEvent` | Event container with metadata and test data                   |
| `event.metadata`  | `ReportMetadata`  | CI/CD, runner, pipeline, job, source, and product information |
| `event.test`      | `TestReport`      | Test execution data with results, properties, and timings     |

### Benefits of Protocol Buffer Schema

The Protocol Buffer definition provides several advantages over JSON-only documentation:

- **Strong Typing**: Each field has a defined type (string, int32, float, etc.)
- **Schema Validation**: Automatic validation of event structure
- **Documentation**: Built-in field documentation and comments
- **Cross-Language Support**: Generate code for multiple programming languages
- **Backwards Compatibility**: Versioning support with field numbering
- **Performance**: More efficient serialization than JSON
- **Composition Pattern**:  To eliminate field duplication:
    1. `TestStatistics` message is shared by `TestReport`, `TestCase` and `TestSuite`.
    2. `ExecStatus` message is shared by `Job` and `Pipeline`.

> **Note**: The Protocol Buffer schema uses composition with `TestStatistics` to share common fields between test-related messages, following protobuf best practices for avoiding field duplication.

### Detailed Schema Components

**ReportMetadata Structure:**

```protobuf
message ReportMetadata {
    bool is_ci = 1;
    CI ci = 2;
    Pipeline pipeline = 3;
    Job job = 4;
    Source source = 5;
    Product product = 6;
}
```

**CI System Structure:**

```protobuf
message CI {
    string url = 1;
    string type = 2;
    CIRunner runner = 3;
}

message CIRunner {
    string name = 1;
    optional string url = 2;
    repeated CIRunnerPropertyString properties_string = 3;
    repeated CIRunnerPropertyInt properties_int = 4;
    repeated CIRunnerPropertyStringArray properties_string_array = 5;
}
```

**Test Statistics Composition:**
```protobuf
message TestStatistics {
    int32 tests = 1;        // Total number of tests
    int32 skipped = 2;      // Number of skipped tests
    int32 errors = 3;       // Number of tests with errors
    int32 failures = 4;     // Number of failed tests
    float time = 5;         // Total execution time
}
```

**TestReport Structure:**
```protobuf
message TestReport {
    TestStatistics stats = 1;           // Overall test run statistics
    repeated TestSuite test_suites = 3;  // Individual test suites
}

message TestSuite {
    string name = 1;                    // Suite name
    TestStatistics stats = 2;           // Suite-level statistics  
    string timestamp = 8;               // Suite execution timestamp
    repeated TestSuiteProperty properties = 9;  // Suite properties
    repeated TestCase test_cases = 10;   // Individual test cases
}

message TestCase {
    string name = 1;                    // Test case name
    string classname = 2;               // Test class name
    TestStatistics stats = 3;           // Case-level statistics
    string system_err = 4;              // System error output
    TestResult result = 5;              // Test result details
}
```

---

## Metadata Structure

The metadata section provides comprehensive information about the CI environment, organized into logical sections:

```yaml
metadata:
  ci:                    # CI system details
    type: "<ci_type>"    # jenkins, dci, github, etc.
    url: "<ci_url>"      # CI system base URL
    runner:              # Execution environment information
      name: "<runner_name>"
      labels: []         # Runner capabilities/labels
      # Hardware and software details
  
  pipeline:              # Pipeline information (when applicable)
    id: "<pipeline_id>"
    url: "<pipeline_url>"
    # Pipeline-specific metadata
  
  job:                   # Job/Build information
    name: "<job_name>"
    url: "<job_url>"
    id: "<job_id>"
    # Job execution details
  
  source:                # Source code information
    repository: "<repo_url>"
    branch: "<branch_name>"
    sha: "<commit_hash>"
    change:              # Pull request/merge request details
      id: "<change_id>"
      author: "<author_name>"
      url: "<change_url>"
      # Change-specific information
  
  product:               # Product under test information
    name: "<product_name>"
    version: "<version>"
    # Product-specific metadata
```

### Metadata Coordinate System

The metadata uses a hierarchical coordinate system for easy querying:

| Event Coordinate | Description | Example Key | Final Coordinate |
|------------------|-------------|-------------|------------------|
| `.ci[]` | CI system info | `ci_url` | `.ci.url` |
| `.ci.runner[]` | Runner details | `ci_runner_name` | `.ci.runner.name` |
| `.pipeline[]` | Pipeline info | `pipeline_id` | `.pipeline.id` |
| `.job[]` | Job information | `job_url` | `.job.url` |
| `.source[]` | Source code | `source_sha` | `.source.sha` |
| `.source.change[]` | Change details | `source_change_author` | `.source.change.author` |
| `.product[]` | Product info | `product_name` | `.product.name` |

---

## CI System Integration

### Jenkins Integration

Jenkins builds expose metadata through environment variables that are mapped to the standardized event structure.

#### Key Environment Variables

**CI System Information:**

- `JENKINS_URL`: Base URL of the Jenkins instance
- `NODE_NAME`: Agent/controller name where build runs
- `WORKSPACE`: Build workspace directory
- `EXECUTOR_NUMBER`: Unique executor identifier
- `BUILD_CAUSE`: Comma-separated list of build triggers

**Job Information:**

- `JOB_NAME`: Jenkins job name
- `JOB_URL`: Job URL
- `BUILD_NUMBER`: Unique build number
- `BUILD_ID`: Build identifier (usually same as BUILD_NUMBER)
- `BUILD_TAG`: Unique tag combining job name and build number
- `BUILD_URL`: URL to specific build results

**Source Code Information:**

- `GIT_COMMIT`: Full SHA-1 hash of current commit
- `GIT_BRANCH`: Git branch name (e.g., origin/master)
- `GIT_URL`: Remote Git repository URL
- `GIT_LOCAL_BRANCH`: Local branch name (if applicable)
- `GIT_PREVIOUS_COMMIT`: Previous commit SHA-1
- `GIT_PREVIOUS_SUCCESSFUL_COMMIT`: Last successful build commit SHA-1
- `GIT_COMMITTER_NAME` / `GIT_AUTHOR_NAME`: Committer/author names
- `GIT_COMMITTER_EMAIL` / `GIT_AUTHOR_EMAIL`: Committer/author emails

**Change Information:**

*GitHub Pull Requests:*

- `CHANGE_ID` / `PULL_REQUEST_ID`: Pull request identifier
- `CHANGE_BRANCH`: Source branch name
- `CHANGE_TARGET`: Target branch name
- `CHANGE_FORK`: Fork repository name
- `CHANGE_URL`: Pull request URL
- `CHANGE_AUTHOR`: PR author username
- `CHANGE_AUTHOR_DISPLAY_NAME`: PR author display name

*GitLab Merge Requests:*

- `CHANGE_ID` / `GITLAB_MERGE_REQUEST_IID`: Merge request identifier
- `GITLAB_MERGE_REQUEST_SOURCE_BRANCH`: Source branch
- `GITLAB_MERGE_REQUEST_TARGET_BRANCH`: Target branch
- `GITLAB_MERGE_REQUEST_LAST_COMMIT_SHA`: Last commit SHA
- `GITLAB_USER_NAME`: MR author name
- `GITLAB_USER_EMAIL`: MR author email

**Runner Information:**

- `NODE_NAME`: Runner name
- `NODE_LABELS`: Space-separated list of node labels

> **Note**: Set `NODE_LABELS` on Jenkins nodes using the provided script or equivalent for proper runner metadata collection.

#### Jenkins-Specific Considerations

- **Pipeline Object**: Jenkins doesn't have a native "pipeline" concept, so `pipeline: {}` by default
- **Product Information**: Can be derived from job parameters and file paths analysis
- **Parent/Caller Jobs**: Future enhancement may populate pipeline data with parent job metadata

### DCI Integration

Distributed CI (DCI) provides a different approach to CI metadata collection since it stores completed process information rather than running live processes.

#### DCI Terminology

| DCI Term | Domain | Meaning |
|----------|--------|---------|
| **product** | RelEng | Product identifier |
| **topic** | RelEng | Minor release stream |
| **component** | RelEng | Version stream |
| **team** | RelEng | Access control for product/topic/component/remoteci/agent/pipeline/job |
| **job** | Execution | Individual job execution |
| **pipeline** | Execution | Job triggering other jobs |
| **agent** | Execution | Execution node |

#### DCI vs. Other CI Systems

| DCI | Jenkins | GitHub | GitLab | Prow |
|-----|---------|--------|--------|------|
| job | job | job | job | job |
| pipeline | job triggering other jobs | workflow | pipeline | pipeline |
| agent | node | runner | runner | node |

#### DCI API Integration

**Prerequisites:**

1. Working credentials with DCI service access
2. Team and remoteci information
3. Installed `dcictl` command-line tool

**Setup Process:**

1. Install `dcictl` following the [DCI client README](https://github.com/redhat-cip/python-dciclient/blob/master/README.md)
2. Access DCI web interface
3. Navigate to "Remotecis" section
4. Search for your remoteci name
5. Download `dcirc.sh` configuration file

**Configuration File Structure:**

```bash
DCI_CLIENT_ID='remoteci/<UUID>'
DCI_API_SECRET='<API_SECRET>'
DCI_CS_URL='https://api.distributed-ci.io/'
export DCI_CLIENT_ID DCI_API_SECRET DCI_CS_URL
```

**Using dcictl:**

```bash
# Source the configuration
source dcirc.sh

# Query examples using Elasticsearch DSL syntax
dcictl remoteci-list --query "(eq(name,${myteam}))"
dcictl job-list --query "and(eq(team_id,${my_team_id}),eq(topic_id,${my_topic_id}))"

# Useful parameters
--query        # Elasticsearch DSL syntax
--where        # Alternative syntax, e.g., "tags in [bla, blah, blee]"
--limit        # Items per page
--format json  # JSON output for parsing
```

#### DCI Metadata Collection

Unlike other CI systems that use environment variables, DCI metadata is obtained through API calls and converted to the standard event format. The metadata is retrieved as JSON and doesn't require dynamic environment processing.

### Environment Variable Mapping

The `env2vars` system provides a flexible framework for mapping CI system environment variables to standardized event metadata.

#### Problem Statement

Different CI systems expose metadata through various mechanisms:
- **Environment variables** (most common)
- **JSON files** referenced by environment variables
- **API endpoints** (like DCI)

Each system uses different terminology and structures, making cross-system analytics challenging.

#### Solution: Normalized Metadata Pipeline

The role implements a three-stage normalization process:

1. **`env2vars` Definition**: Maps environment variables to transition dictionary keys
2. **`trs_vars_dict` Population**: Collects and formats values from environment
3. **Event Metadata Generation**: Transforms transition dictionary to final event structure

#### Implementation Stages

```
Environment Variables → env2vars → trs_vars_dict → event.metadata
```

1. **Development Stage**: Define `env2vars` mappings for each CI system
2. **Runtime Stage**: Populate `trs_vars_dict` from environment variables
3. **Event Generation**: Transform `trs_vars_dict` keys to final metadata structure

#### Variable Definition Structure

Variables are defined in `vars/env2vars/<ci_type>.yml` files:

**Basic String Variable:**

```yaml
env2vars:
  - key: my_key
    var: MY_ENV_VAR
    var_type: str  # Default type, can be omitted
```

**List Variable:**

```yaml
env2vars:
  - key: my_list_key
    var: MY_ENV_LIST_VAR
    var_type: list
    splitter: ['/']  # Default splitter, can be omitted
```

**Dictionary Variable:**

```yaml
env2vars:
  - key: my_dict_key
    var: MY_ENV_DICT_VAR
    var_type: dict
    splitter: [' ', ':']  # Element separator, Key-value separator
```

**Integer Variable:**

```yaml
env2vars:
  - key: my_number
    var: MY_ENV_NUMBER
    var_type: int
```

**Boolean Variable:**

```yaml
env2vars:
  - key: my_bool
    var: MY_BOOL_VAR
    var_type: bool
```

#### Supported Data Types

| Type    | Description     | Example Input                   | Example Output                                |
| ------- | --------------- | ------------------------------- | --------------------------------------------- |
| `str`   | String          | `MY_VAR="hello"`                | `{"key": "hello"}`                            |
| `list`  | String array    | `MY_VAR="a/b/c"`                | `{"key": ["a", "b", "c"]}`                    |
| `dict`  | Flat dictionary | `MY_VAR="os:linux arch:x86_64"` | `{"key": {"os": "linux", "arch": "x86_64"}}`  |
| `int`   | Integer         | `MY_VAR="123"`                  | `{"key": 123}`                                |
| `bool`  | Boolean         | `MY_VAR="true"`                 | `{"key": true}`                               |

#### List Processing

Lists are parsed using configurable separators:

```yaml
# Environment: MY_LIST="item1,item2,item3"
- key: items
  var: MY_LIST
  var_type: list
  splitter: [',']
# Result: {"items": ["item1", "item2", "item3"]}
```

#### Dictionary Processing

Dictionaries support nested key-value pairs:

```yaml
# Environment: MY_DICT="os:linux arch:x86_64 version:1.0"
- key: system_info
  var: MY_DICT
  var_type: dict
  splitter: [' ', ':']  # [element_separator, key_value_separator]
# Result: {"system_info": {"os": "linux", "arch": "x86_64", "version": "1.0"}}
```

---

## Reporting Systems

Reporting systems collect, search, and visualize CI and test data to enable observability and data-driven decision making.

### Benefits

- **Shared Visual Languages**: Consistent dashboards across teams
- **Data-Driven Decisions**: Analytics-based process improvements
- **Cross-System Insights**: Unified view across different CI systems

### Splunk Integration

Splunk serves as the primary reporting backend, providing powerful search, analytics, and visualization capabilities.

#### Event Schema for Splunk

Splunk events follow the corrected structure with an event wrapper containing metadata and test data:

```json
{
    "source": "<team_identifier>",
    "host": "<hostname>",
    "sourcetype": "_json",
    "_time": "<timestamp>", // this attribute is automatically set by splunk
    "event": {
        "metadata": "<metadata_object>",
        "test": "<test_data_object>"
    }
}
```

The structure uses an `event` wrapper to accommodate Splunk's event format requirements while maintaining compatibility with the Protocol Buffer schema definitions.

#### Query Capabilities

The schema supports various query patterns using the event wrapper structure:

**Product-Based Queries:**

- Filter by product: `.event.metadata.product[]` attributes
- Version-specific analysis: `.event.metadata.product.version`

**CI System Queries:**

- CI type filtering: `.event.metadata.ci.type`
- Status-based filtering: `.event.metadata.ci.status`
- Runner-specific queries: `.event.metadata.ci.runner[]`

**Test Result Queries:**

- Test suite results: `.event.test.test_suites[].test_cases[].result.status`
- Test case analysis: `.event.test.test_suites[].test_cases[].name`
- Performance metrics: `.event.test.test_suites[].stats.time`
- Suite-level stats: `.event.test.test_suites[].stats.tests`, `.event.test.test_suites[].stats.failures`
- Overall test stats: `.event.test.stats.tests`, `.event.test.stats.failures`, `.event.test.stats.errors`
- Individual test case stats: `.event.test.test_suites[].test_cases[].stats.time`

#### Timing Considerations

All timing data uses consistent time sources to ensure accurate correlation:

1. **CI Process Timings**: Pipeline, job, and step durations
2. **Test Timings**: Test suite and case execution times

> **Important**: CI systems must be properly configured with NTP/PTP for accurate timing correlation.

#### Test Data Structure

**Test Report Summary (per Protocol Buffer schema):**

```json
{
    "test": {
        "stats": {
            "tests": 10,
            "skipped": 1,
            "errors": 0,
            "failures": 2,
            "time": 45.67
        },
        "test_suites": [...]
    }
}
```

**Test Suite Structure (per Protocol Buffer schema):**
```json
{
    "name": "test_suite_name",
    "stats": {
        "tests": 5,
        "skipped": 0,
        "errors": 0,
        "failures": 1,
        "time": 12.34
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "properties": [
        {"name": "category", "value": "unit"},
        {"name": "environment", "value": "test"}
    ],
    "test_cases": [...]
}
```

**Test Case Structure (per Protocol Buffer schema):**
```json
{
    "name": "test_method_name",
    "classname": "TestClass",
    "stats": {
        "tests": 1,
        "skipped": 0,
        "errors": 0,
        "failures": 1,
        "time": 2.45
    },
    "system_err": "",
    "result": {
        "status": "failure",
        "message": "Assertion failed: Expected 'true' but got 'false'"
    }
}
```

### Benefits of TestStatistics Composition

The new composition pattern provides several advantages:

- **Consistent Structure**: All test-related entities (TestReport, TestSuite, TestCase) share the same statistics structure
- **Reduced Duplication**: Common fields are defined once in `TestStatistics`
- **Type Safety**: Strong typing ensures consistent data types across all levels
- **Easy Aggregation**: Statistics can be easily rolled up from test cases to suites to overall report
- **Maintainability**: Changes to statistics fields only need to be made in one place

---

## Implementation Guide

### Getting Started

1. **Choose Your CI System**: Identify which CI system you're integrating with
2. **Configure Variables**: Set up the appropriate `env2vars` configuration
3. **Test Metadata Collection**: Verify environment variables are properly mapped
4. **Configure Reporting**: Set up your reporting backend (Splunk, etc.)
5. **Run Integration Tests**: Validate end-to-end event generation and delivery

### Best Practices

- **Consistent Timing**: Ensure all CI systems use synchronized time sources
- **Comprehensive Metadata**: Include all relevant environment variables for your use case
- **Test Data Quality**: Validate JUnit report format compliance
- **Monitoring**: Set up alerts for failed event deliveries
- **Documentation**: Maintain clear documentation of custom variable mappings

### Troubleshooting

**Common Issues:**
- **Missing Environment Variables**: Check CI system configuration and permissions
- **Incorrect Data Types**: Verify `env2vars` type specifications
- **Timing Discrepancies**: Ensure NTP/PTP synchronization across systems
- **Failed Event Delivery**: Check reporting system connectivity and credentials

### Future Enhancements

- **Additional CI Systems**: Prow, Tekton, and other emerging CI platforms
- **Enhanced Product Detection**: Automatic product identification from file paths and job parameters
- **Pipeline Relationships**: Better parent/child job relationship mapping
- **Real-time Streaming**: Support for real-time event streaming to reporting systems

---

## Conclusion

The `test_report_send` role provides a comprehensive solution for normalizing CI metadata and test results across multiple CI systems. By implementing standardized event structures and flexible variable mapping, it enables powerful cross-system analytics and observability.

### Key Resources

- **Protocol Buffer Schema**: See [`event.proto`](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/test_report_send/protos/event.proto) for the complete, formal definition of the event structure
- **Environment Variable Mappings**: Individual configuration files in the `vars/env2vars/` directory
- **Implementation Examples**: Customize the mappings according to your CI environment and reporting requirements

The Protocol Buffer schema serves as the single source of truth for event structure, ensuring type safety and consistency across all implementations. 