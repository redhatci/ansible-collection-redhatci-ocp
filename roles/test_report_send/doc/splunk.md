# Splunk

## Conventions

- Example queries are presented in `jq` or `yq` -like manner.
- variables are presented in monospace like `this_one`

### Abbreviations

- SUT = system under test

## The event contains the following

1. CI system details
   - type
   - endpoints about the system and specific runner
   - ci processes' components (pipelines, chains, jobs, steps) and their ids/timings
   - triggering info (about how the ci was invoked)
   - results (how have they completed)
2. SUT info: H/W (architecture), and software info (OS, product/component incl. releases/versions)
3. Source code information (repository, branch, pr/mr, commit hashes, ownership info of both the code and the event)
4. Test information (JUnit test reports converted into JSON)
5. Additional future information

## Schema (objectives) and background

It should provide:

   1. Enough data attributes to support required queries for visualization and observability
   2. Minimum data points
   3. Ease of extension

The schema needs to support querying by any of the following terms

### Metadata (collected dynamically)

- product release(s)
- SUT details (os, architecture)
- team(s)
- ci status (pipeline/job/step)

### Test data (collected from test reports)

- tests:
  - run (status, counters, start, duration)
    - suite (status, counters, start, duration)
      - case (status, counters, start, duration)
        - for failures - more info

### The importance of Timing

Everything with timing data must be selected by those time ranges.
Thus, to avoid confusion, the time range search should use only two sources of timing:

1. ci process timings
2. test timings

We need to rely on these timings, so all the CI systems need to be properly set up using ntp/ptp.

## Event Schema (structure)

Due to the above, the following is proposed

### Metadata (dynamically obtained for each event)

   1. ci
      1. general
         1. type
         2. endpoints
      2. runner
         1. s/w SUT
         2. h/w SUT
      3. object:
         1. pipeline
         2. job
         3. step
      4. trigger
   2. product info
      1. release
      2. components
   3. source code:
      1. repo
      2. branch
      3. merge/pull request
      4. author

### Test data

1. test report info (obtained from ci process artifact files)
   1. run
      1. stats
      1. suites, for each suite:
         1. stats
         1. cases for each case
            1. stats
            1. errors

### Top-down structure

#### Splunk event structure

This structure is sent to splunk.

```json
{
    "source": "<str>", // type of information signifying team/channel 
    "host": "<hostname>", // the host or container or service sending the data
    "sourcetype": "_json",
    "_time": <timestamp>, // event emission time stamp, note it may happen AFTER event occurrence.
    "event": <trs_event>, // event data dictionary
}
```

The most interesting structure here is `trs_event`, it also has structure of:

```json
{
  "metadata": <trs_meta_data>, 
  "test": <trs_test_data>
}

```

Splunk event structure is sent to splunk as json and needs to allow queries of the following sorts

1. Select events by product `.metadata.product[]` attributes
2. Filter events by any metadata attribute, for example `.metadata.ci.type`  completed with specific status
