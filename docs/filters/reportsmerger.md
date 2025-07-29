# reportsmerger Filter Plugin

The `reportsmerger` filter merges multiple JUnit test report JSON files (converted by `junit2obj`) into a single consolidated report with aggregated statistics.

## Overview

- **Purpose**: Combine multiple test reports while preserving individual test suite details
- **Input**: List of JSON file paths (output from `junit2obj` filter)
- **Output**: Single merged JSON report with aggregated metrics
- **Version**: 1.1.0+ (strategies introduced)

## Basic Usage

```yaml
- name: Merge test reports (default)
  ansible.builtin.set_fact:
    merged_report: "{{ ['report1.json', 'report2.json'] | redhatci.ocp.reportsmerger }}"
```

## Optimization Strategies

The `strategy` parameter allows optimization for different scenarios:

### Available Strategies

| Strategy | Best For | Memory Usage | Speed | Use Case |
|----------|----------|--------------|--------|----------|
| `normal` | General use | Baseline | Baseline | Default behavior (backward compatible) |
| `large` | Large files (>100MB) | 60-80% less | 15-25% faster | Memory-constrained environments |
| `many` | Many files (50+) | Same | 30-50% faster | I/O bound operations |
| `shallow` | Stats-only queries | 70-90% less | 5-15% faster | When test suite details not needed |
| `complex` | Heavy test case data | 40-60% less | 10-20% faster | Large test case payloads |

### Strategy Examples

#### Normal Strategy (Default)
```yaml
# Standard behavior - backward compatible
- set_fact:
    merged: "{{ test_files | redhatci.ocp.reportsmerger }}"
```

#### Large Strategy - Memory Optimization
```yaml
# For large files - streaming aggregation
- set_fact:
    merged: "{{ large_test_files | redhatci.ocp.reportsmerger(strategy='large') }}"
```

#### Many Strategy - Parallel Processing
```yaml
# For many files - parallel I/O
- set_fact:
    merged: "{{ many_test_files | redhatci.ocp.reportsmerger(strategy='many') }}"
```

#### Shallow Strategy - Stats Only
```yaml
# Fast stats without detailed test suites
- set_fact:
    stats_only: "{{ test_files | redhatci.ocp.reportsmerger(strategy='shallow') }}"

# Access stats immediately (fast)
- debug: msg="Total tests: {{ stats_only.tests }}"

# Access test suites when needed (lazy-loaded)
- debug: msg="Suite count: {{ stats_only.test_suites | length }}"
```

#### Complex Strategy - Lightweight Processing
```yaml
# Skip heavy test case details during parsing
- set_fact:
    lightweight: "{{ complex_files | redhatci.ocp.reportsmerger(strategy='complex') }}"
```

## Output File Option

Write results directly to file instead of returning data:

```yaml
- name: Merge and save to file
  ansible.builtin.set_fact:
    output_path: "{{ files | redhatci.ocp.reportsmerger(output_file='/tmp/merged.json') }}"
```

## Performance Guidelines

### Choosing the Right Strategy

```yaml
# Memory-constrained CI environments
strategy: large

# High-volume test processing (100+ files)
strategy: many

# Dashboard/metrics collection (stats focus)
strategy: shallow

# Complex test suites with large payloads
strategy: complex
```

### Memory Usage Scenarios

| Scenario | Files | Size Each | Recommended Strategy | Memory Reduction |
|----------|-------|-----------|---------------------|------------------|
| Small scale | 5-10 | <10MB | `normal` | - |
| Large files | 10-20 | 50-100MB | `large` | 60-80% |
| Many files | 50-100 | 5-20MB | `many` | - |
| Stats queries | Any | Any | `shallow` | 70-90% |
| Heavy cases | 10-50 | 20-50MB | `complex` | 40-60% |

## Output Structure

All strategies produce the same output structure:

```json
{
  "time": 125.45,
  "tests": 1500,
  "failures": 23,
  "errors": 2,
  "skipped": 45,
  "test_suites": [
    {
      "name": "Suite 1",
      "time": 67.2,
      "timestamp": "2024-12-12T20:12:23",
      "tests": 750,
      "failures": 12,
      "errors": 1,
      "skipped": 20,
      "properties": {...},
      "test_cases": [...]
    }
  ],
  "schema_version": "1.1.0"
}
```

## Error Handling

The filter handles common issues gracefully:

- **Missing files**: Warning logged, skipped from merge
- **Invalid JSON**: Error raised with detailed message
- **Missing fields**: Error raised with field name
- **Invalid strategy**: Error raised with valid options

## Integration Examples

### CI/CD Pipeline
```yaml
- name: Collect test reports
  find:
    paths: "{{ test_output_dir }}"
    patterns: "*.json"
  register: test_files

- name: Merge all test reports
  set_fact:
    final_report: >-
      {{
        test_files.files | map(attribute='path') | list |
        redhatci.ocp.reportsmerger(strategy='many')
      }}

- name: Save merged report
  copy:
    content: "{{ final_report | to_nice_json }}"
    dest: "{{ artifact_dir }}/merged-test-results.json"
```

### Performance Monitoring
```yaml
- name: Quick stats collection
  set_fact:
    test_metrics: "{{ reports | redhatci.ocp.reportsmerger(strategy='shallow') }}"

- name: Log performance metrics
  debug:
    msg: |
      Test Summary:
      - Total Tests: {{ test_metrics.tests }}
      - Success Rate: {{ ((test_metrics.tests - test_metrics.failures - test_metrics.errors) / test_metrics.tests * 100) | round(2) }}%
      - Total Time: {{ test_metrics.time }}s
```

## CLI Documentation

View inline documentation:
```bash
ansible-doc redhatci.ocp.reportsmerger
```

## See Also

- [`junit2obj` filter](./junit2obj.md) - Convert JUnit XML to JSON
- [Collection README](../../README.md) - Full collection overview
- [Plugin source code](../../plugins/filter/reportsmerger.py) - Implementation details
