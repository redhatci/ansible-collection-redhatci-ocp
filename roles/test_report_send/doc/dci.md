# CI: Distributed CI (DCI)

The DCI API endpoint is [https://distributed-ci.io](https://distributed-ci.io).

## DCI Terminology overview

DCI introduces several unique concepts compared to other CI systems:

| DCI term   | LC domain | meaning                                                               |
| ---------- | --------- | --------------------------------------------------------------------- |
| product    | RelEng    | product                                                               |
| topic      | RelEng    | minor release stream                                                  |
| component  | RelEng    | version stream                                                        |
| team       | RelEng    | ACL for `[product\|topic\|component\|remoteci\|agent\|pipeline\|job]` |

### Mapping DCI to Other CI Systems

DCI concepts aligned with common CI terminology:

| DCI      | Jenkins                     | GitHub   | GitLab   | Prow     |
| -------- | --------------------------- | -------- | -------- | -------- |
| job      | job                         | job      | job      | job      |
| pipeline | job triggering other job(s) | workflow | pipeline | pipeline |
| agent    | node                        | runner   | runner   | node     |

## Dynamic environment to metadata conversion

In this DCI use case, we do not need to dynamically process the environment.
When data from DCI reaches us, we can get the metadata from its API as JSON.

### How to obtain data using `dcictl`

#### Prerequisites

1. Working credential with access to DCI service and the components you're planning to work with
2. Information about `team` and `remoteci`

#### Set up

1. See the [dciclient README](https://github.com/redhat-cip/python-dciclient/blob/master/README.md)  
   and install the `dcictl` command-line tool.
2. Browse to DCI via the web
3. Login with credentials, go to the left hand to `Remotecis`
4. In the search field, type `remoteci` name
5. Download `dcirc.sh` from the **"Remotecis"** page

The contents of `dcirc.sh` file should look like this:

```bash
DCI_CLIENT_ID='remoteci/<UUID{lowercase uuid}>'
DCI_API_SECRET='<API_SECRET{random alphanumeric (upper/lower) string 64 chars long}>'
DCI_CS_URL='https://api.distributed-ci.io/'
export DCI_CLIENT_ID DCI_API_SECRET DCI_CS_URL
```

NOTE: the above data is not real.

#### Running dcictl

Before running `dcictl`, the script `dcirc.sh` needs to be sourced (to set up the environment variables).

`dcictl` allows query of the DCI API
The syntax is: `dcictl <command> <params>`
The most interesting parameters are:

### Existing commands

Run: `dcictl --help`

#### Running commands

The parameter `--query` uses ES (elastic search) DSL syntax. Examples:

1. Search by `myteam` name: `dcictl remoteci-list --query "(eq(name,${myteam}))"`
1. Search by TeamId: `my_team_id` and TopicId: `my_topic_id`: `dcictl job-list --query "and(eq(team_id,${my_team_id}),eq(topic_id,${my_topic_id}))"`
1. Sometimes, to list a specific object, you need to gather all its sub-objects via `dcictl`.

##### Additional details

- All item commands (e.g., `<bla>-list`) support the `name` property.  
- The `--where` parameter uses a different syntax, e.g., `tags in [bla, blah, blee]`.  
- The `--limit` parameter lets you set how many items per page are fetched in a single command.  
- The global `--format json` option is very convenient for parsing.  
