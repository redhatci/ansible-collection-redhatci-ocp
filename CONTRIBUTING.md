# redhatci.ocp

## Prerequisites

### Clonning the repository

To be able to [run the sanity tests](#running-the-sanity-tests-locally), the recommended way to extract the repository is like this:

```ShellSession
$ cd <your workspace>
$ mkdir -p ansible_collections/redhatci
$ cd ansible_collections/redhatci
$ git clone git@github.com:redhatci/ansible-collection-redhatci-ocp.git ocp
$ cd ocp
...
```

### Sign commits

[Follow this documentation to sign your commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)

For traceability and delivering software in a secure manner this repository requires *all* the commits to be signed (not to be confused with sign-off). Because of that, don't edit or rebase from the GitHub UI as it will not be signed doing it this way.

### Running the sanity tests locally

The sanity tests are run using the [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html) tool. It comes from the `ansible-core` package. This is what is run in [the CI pipeline](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/.github/workflows/pr.yml#L40).

```ShellSession
$ ansible-test sanity --verbose --docker --color --coverage --failure-ok
```

Legacy code is expected to fail some sanity tests. The ask is to not introduce new failures and fix the errors in the legacy code when you are modifying it. It is an iterative process to clean up the legacy code.

## Pull Requests

The collection is using the [GitHub Flow](https://guides.github.com/introduction/flow/) for the development. The main branch is `main`. The `main` branch is protected and requires a PR to be merged. The PRs are reviewed by the maintainers of the collection.

Keep the PRs small and focused on a single topic. Write a [good commit message](https://cbea.ms/git-commit/). It is easier to review and merge. It also helps to keep the git history clean. Keep as few commits as possible.

When updating a PR follow these approaches:

1. Use `git commit --amend` and `git push --force` to update the PR. It will update the PR automatically. Do this when you iterate by yourself on a PR. When someone else has reviewed the PR, it is better to create a new commit to keep the history of the PR.
2. Squash the commits when you are ready to merge the PR.

PRs can be created as a [Draft](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests), use this when the change is not yet ready for review or set a PR to Draft if it needs more time before continuing with the review process.

### AI-Assisted Development Guidelines

When using AI tools for contributions, prioritize human oversight, code quality, and security compliance.

#### Human Validation Required

* **Treat AI output as suggestions, not final code** - you must verify and validate all generated content
* **Never blindly trust AI agents** - apply your judgment and expertise to all suggestions
* **Understand all code before submitting** - consult experts if AI generates code outside your expertise
* **Thoroughly review and test** - AI can introduce vulnerabilities or generate incorrect code

#### Review Considerations

* **Keep changes small and focused** - large AI-generated changes are harder and riskier to review
* **Mark substantial AI-assisted content** for transparency and focused review

#### Documentation

* **Identify AI usage** in commit messages or PR descriptions using trailers:
  ```
  Assisted-by: [AI agent name]
  ```

#### Security and Compliance

* **Use only approved AI assistants** validated through proper AI assessments
* **Never input sensitive data** - API keys, passwords, credentials, or proprietary code
* **Sanitize code snippets** and use synthetic data during development

### Ready for review

Your PR is considered ready for review if all the CI checks are green. If you don't want a review yet, convert your PR to a Draft.

## Bumping the version

The collection is continuously built and published to [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/). The versioning scheme used is [Semantic Versioning](https://semver.org/) with an automatic `PATCH` number to allow to publish automatically. This PATCH  number is the UNIX epoch time of the last commit. This allows to publish a new version of the collection every time a change is merged to the `main` branch.

The version is defined in the `galaxy.yml` file and `ansible-collection-redhatci-ocp.spec`. To bump the version (`MAJOR` or `MINOR`), edit these files and commit the change.

Edit `MAJOR` when there are breaking changes in the collection. Edit `MINOR` when there are new features added to the collection.

## CI pipelines

The collection has multiple CI pipelines that run on every PR:

- PR pipeline: [`.github/workflows/pr.yml`](../.github/workflows/pr.yml) that runs the sanity tests and Ansible lint. It fails if there is any regression. It also runs a check on the PR Dependencies (`Depends-On:` lines in the commit message) to make sure that the dependencies are merged before the PR. Tests can be run locally:
  - For Ansible lint tests, run [`./hack/ansible-lint.sh -d`](hack/ansible-lint.sh).
  - For Sanity, Integration and Unit tests, run [`./hack/run_ansible_test.sh`](hack/run_ansible_test.sh).
  - For Doc checks, run [`./hack/check_doc.sh`](hack/check_doc.sh).
  - For version checks, run [`./hack/check_version.sh`](hack/check_version.sh).
- DCI BOS2 pipeline: [`.github/workflows/dci.yml`](../.github/workflows/dci.yml) that runs a DCI job to test the collection in a virtual environment at the BOS2 Telco Partner CI lab. It is triggered only when a change is modifying files in the `/roles/` directory.
- DCI Dallas pipeline: run DCI jobs on a baremetal cluster in the Telco Partner CI Dallas lab. It is triggered automatically only when changes are modifying files in the `role/cnf-cert` or `roles/preflight` directories.
- RPM build pipeline (dci/check). This is managed by the Zuul CI on <https://gateway-cloud-softwarefactory.apps.ocp.cloud.ci.centos.org/>. It builds rpm for el8 and el9.

To specify which DCI lab to use and which resources to use, you can use the following strings in the descrption of the PR:

  * `TestDallas`: baremetal clusters in the Dallas lab.
  * `TestDallasHybrid`: hybrid clusters with a virtualized control-plane in the Dallas Lab.
  * `TestDallasWorkload`: workload on a pre-installed baremetal cluster in Dallas.
  * `TestBos2`: virtual setup in the BOS2 lab.
  * `TestBos2Sno`: virtual SNO setup in the BOS2 lab.
  * `TestBos2SnoBaremetal`: baremetal SNO node in the BOS2 lab.

The following `Test-Hints` can be specified if needed in the description of the PR:

  * `Test-Hint: no-check` when no test is needed in DCI. For a doc only change this is detected automatically.
  * `Test-Hint: force-check` to bypass the automatic no code change detection. Useful for CI testing.

Examples:

```yaml
TestDallas: ocp-4.14-vanilla example-cnf
TestDallasWorkload: preflight-green
TestBos2: virt control-plane
Test-Hint: force-check
```

At least one check needs to pass for the PR to be validated.

Reach out to the Telco Partner CI team if you need more information.

### Merge Queue

There is a set of CI pipelines that are run just before merging by [the merge queue mechanism of GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue). This allows to validate the merged PR before pushing them to main. This is important to avoid parallel merge of PRs that would break the collection.


## Issues

We welcome feedback! Open [issues](https://github.com/redhatci/ansible-collection-redhatci-ocp/issues) filling out as much as possible in the issue template. Providing an accurate way of reproducing the issue is critical in helping us identify the problem quicker.

Before opening a new issue, please use the search feature to see if someone has not reported something similar. If there is an open issue you're experimenting and have additional information, please comment. Using "thumbs up" in an issue help us to give an indication on how many people is facing that problem.
