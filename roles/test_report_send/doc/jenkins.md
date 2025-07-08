# CI: Jenkins

Current or past runs of jenkins jobs are called "builds".
During a jenkins job build, the executor node process sets up multiple environment variables for its child processes.
Build's parameters are also seen by the processes as environment variables.

## Environment to metadata conversion

## Metadata Sections

Following the metadata schema explained in [metadata.md](metadata.md), and described below are the metadata sections we're collecting when running in jenkins.

### CI

* `NODE_NAME`: The name of the agent (or controller) where the build is running.
* `WORKSPACE`: The absolute path to the directory where the job's files and outputs are stored during the build process.
* `JENKINS_HOME`: The directory where Jenkins stores its configuration, build history, and other data.
* `EXECUTOR_NUMBER`: The unique number that identifies the current executor (among executors of the same machine) performing this build
* `BUILD_CAUSE`:  A comma-separated list of causes for the build (e.g., `SCMTRIGGER,MANUALTRIGGER,UPSTREAMTRIGGER`).
  Individual causes are also exposed as separate environment variables:
  * `BUILD_CAUSE_SCMTRIGGER=true`
  * `BUILD_CAUSE_USERIDCAUSE=true`
  * etc.
* `JENKINS_URL`: The base URL of the Jenkins instance.

### Runner

* `NODE_NAME` (name).
* `NODE_LABELS` (space-separated list of labels).

The `NODE_LABELS` variable should be set on the Jenkins nodes via the [script](scripts/jenkins_node_labels.sh) or equivalent.

### Pipeline

By default, Jenkins does not have an object of "pipeline", so in the metadata we will have `pipeline: {}`.
However, similar functionality can refer to the parent (or caller) job that triggered this and/or other (sibling) jobs, so in future we may decide to populate `pipeline` with that parent/caller job's metadata.

### Job

* `JOB_NAME`: The name of the Jenkins job.
* `JOB_URL`: The URL of the Jenkins job.
* `BUILD_NUMBER`: The unique build number for the current run (e.g., `153`).
* `BUILD_ID`: The current build ID, usually identical to BUILD_NUMBER for recent Jenkins versions.
* `BUILD_TAG`: A unique tag combining the job name and build number (e.g., `jenkins-${JOB_NAME}-${BUILD_NUMBER}`).
* `BUILD_URL`: The URL where the results of this specific build can be found.

### Source

* `GIT_COMMIT`: The full `SHA-1` hash of the current Git commit being built.
* `GIT_BRANCH`: The name of the Git branch being built (e.g., origin/master, feature/my-branch).
* `GIT_URL`: The URL of the remote Git repository.
* `GIT_LOCAL_BRANCH`: If a specific local branch is checked out, this variable will contain its name.
* `GIT_PREVIOUS_COMMIT`: The `SHA-1` hash of the previous commit on the current branch.
* `GIT_PREVIOUS_SUCCESSFUL_COMMIT`: The `SHA-1` hash of the commit of the last successful build on the current branch.
* `GIT_COMMITTER_NAME` / `GIT_AUTHOR_NAME`: The name of the committer/author of the current Git commit.
* `GIT_COMMITTER_EMAIL` / `GIT_AUTHOR_EMAIL`: The email of the committer/author of the current Git commit.

#### The Change: Pull Request/Merge Request/ChangeId

* `CHANGE_ID`: for GitHub it is PR, for GitLab it is MR, for Gerrit it is ChangeId.
* `PULL_REQUEST_ID`: GitHub term
* `GITLAB_MERGE_REQUEST_IID`: GitLab term

##### GitHub Change Info (PR)

* `CHANGE_BRANCH`: source branch name of the PR
* `CHANGE_TARGET`: target branch of the PR
* `CHANGE_FORK`: the fork repository name
* `CHANGE_URL`: the URL to the PR

###### Author (PR)

* `CHANGE_AUTHOR`: the author of the PR
* `CHANGE_AUTHOR_DISPLAY_NAME`: the display name of the PR author

##### GitLab Change Info (MR)

* `GITLAB_MERGE_REQUEST_SOURCE_BRANCH`: source branch of the MR
* `GITLAB_MERGE_REQUEST_TARGET_BRANCH`: target branch of the MR
* `GITLAB_MERGE_REQUEST_LAST_COMMIT_SHA`: last sha of the MR

###### Author (MR)

* `GITLAB_USER_NAME`: The merge request author's name.
* `GITLAB_USER_EMAIL`: The merge request author's email.

### Product

Jenkins by default does not have this construct, so in the metadata we can assign `product: {}`,
However similar functionality can refer to a job that triggers other jobs.

* **UPD**: We will probably add this information by analyzing files paths and job parameters
