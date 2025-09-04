# Filter Plugins Documentation

This directory contains detailed documentation for all filter plugins in the `redhatci.ocp` collection.

## Available Filters

| Filter | Purpose | Documentation |
|--------|---------|---------------|
| `junit2dict` | Transform JUnit XML to dictionary | [View CLI docs](../../plugins/filter/junit2dict.py) |
| `junit2obj` | Transform JUnit XML to JSON object | [View CLI docs](../../plugins/filter/junit2obj.py) |
| `ocp_compatibility` | Parse deprecated/to-be-deprecated APIs | [View CLI docs](../../plugins/filter/ocp_compatibility.py) |
| `reportsmerger` | Merge multiple test reports with optimization strategies | [📖 Detailed docs](./reportsmerger.md) |
| `regex_diff` | Find differences between two lists using regex | [View CLI docs](../../plugins/filter/regex_diff.py) |

## Quick Reference

### View CLI Documentation
```bash
# View any filter's inline documentation
ansible-doc redhatci.ocp.<filter_name>

# Examples:
ansible-doc redhatci.ocp.reportsmerger
ansible-doc redhatci.ocp.junit2obj
```

### Common Usage Patterns

#### Test Report Processing Pipeline
```yaml
# 1. Convert JUnit XML to JSON
- set_fact:
    json_reports: "{{ xml_files | map('redhatci.ocp.junit2obj') | list }}"

# 2. Merge multiple reports with optimization
- set_fact:
    merged_report: "{{ json_files | redhatci.ocp.reportsmerger(strategy='many') }}"
```

#### Performance Optimization
```yaml
# Choose strategy based on your scenario:
strategy: normal    # Default behavior
strategy: large     # Large files (>100MB) - 60-80% memory reduction
strategy: many      # Many files (50+) - 30-50% speed improvement
strategy: shallow   # Stats only - 70-90% memory reduction
strategy: complex   # Heavy test cases - 40-60% memory reduction
```

## Contributing

When adding new filter documentation:

1. **Inline docs**: Always include `DOCUMENTATION`, `EXAMPLES`, and `RETURN` in the plugin file
2. **Detailed docs**: Create `docs/filters/<filter_name>.md` for complex filters
3. **Update this index**: Add entries to the table above
4. **Update main README**: Link to detailed docs in the main collection README

## See Also

- [Collection README](../../README.md) - Main collection documentation
- [Plugin Directory](../../plugins/filter/) - Source code for all filters
