# Development guide

## Cloning the repository

To be able to run the sanity tests, the recommended way to extract the repository is like this:

```ShellSession
$ cd <your workspace>
$ mkdir -p ansible_collections/redhatci
$ cd ansible_collections/redhatci
$ git clone git@github.com:redhatci/ansible-collection-redhatci-ocp.git ocp
$ cd ocp
...
```

## Running the sanity tests locally

The sanity tests are run using the [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html) tool. It comes from the `ansible-core` package. This is what is run in [the CI pipeline](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/.github/workflows/pr.yml#L40).

```ShellSession
$ ansible-test sanity --verbose --docker --color --coverage --failure-ok
```

Legacy code is expected to fail some sanity tests. The ask is to not introduce new failures and fix the errors in the legacy code when you are modifying it. It is an iterative process to clean up the legacy code.

## Pull Requests

The collection is using the [GitHub Flow](https://guides.github.com/introduction/flow/) for the development. The main branch is `main`. The `main` branch is protected and requires a PR to be merged. The PRs are reviewed by the maintainers of the collection.

Keep the PRs small and focused on a single topic. It is easier to review and merge. It also helps to keep the git history clean. Keep as few commits as possible. Here are the 2 things to consider when updating a PR:

1. Use `git commit --amend` and `git push --force` to update the PR. It will update the PR automatically. Do this when you iterate by yourself on a PR. When someone else has reviewed the PR, it is better to create a new commit to keep the history of the PR.
2. Squash the commits when you are ready to merge the PR.

PRs can be created as a [Draft](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests), use this when the change is not yet ready for review or set a PR to Draft if it needs more time before continuing with the review process.

### Ready for review

Your PR is considered ready for review if all the CI checks are green. If you don't want a review yet, convert your PR to a Draft.

### Sign commits

[Sign your commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) for traceability and delivering software in a secure manner. Because of that, don't edit or rebase from the GitHub UI as it will not be signed doing it this way.

## Bumping the version

The collection is continuously built and published to [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/). The versioning scheme used is [Semantic Versioning](https://semver.org/) with an automatic `PATCH` number to allow to publish automatically. This PATCH  number is the UNIX epoch time of the last commit. This allows to publish a new version of the collection every time a change is merged to the `main` branch.

The version is defined in the `galaxy.yml` file and `ansible-collection-redhatci-ocp.spec`. To bump the version (`MAJOR` or `MINOR`), edit these files and commit the change.

Edit `MAJOR` when there are breaking changes in the collection. Edit `MINOR` when there are new features added to the collection.

## CI pipelines

The collection has multiple CI pipelines that run on every PR:

- PR pipeline: [`.github/workflows/pr.yml`](../.github/workflows/pr.yml) that runs the sanity tests and Ansible lint. It fails if there is any regression. It also runs a check on the PR Dependencies (`Depends-On:` lines in the commit message) to make sure that the dependencies are merged before the PR.
- DCI BOS2 pipeline: [`.github/workflows/dci.yml`](../.github/workflows/dci.yml) that runs a DCI job to test the collection in a virtual environment at the BOS2 Telco Partner CI lab. It is triggered only when a change is modifying files in the `/roles/` directory. You can use `Test-Hint*` strings in the PR to modify what is tested. See [the DCI documentation](https://docs.distributed-ci.io/dci-openshift-agent/docs/development/#hints) for more details.
- DCI Dallas pipeline: run DCI jobs on a baremetal cluster in the Telco Partner CI Dallas lab. It is triggered only when changes are modifying files in the `role/cnf-cert` or `roles/preflight` directories.
- RPM build pipeline (local/check). This is managed by the Zuul CI on https://softwarefactory-project.io/. It builds rpm for el8 and el9.

If you are part of the project, you can also use comments in the PR to trigger the baremetal pipelines manually in the Telco Partner CI Dallas lab:

- `check dallas ocp-4.15-vanilla example-cnf`
- `check workload preflight-green`

Reach out to the Telco Partner CI team if you need more information.

### Merge Queue

There is a set of CI pipelines that are run just before merging by [the merge queue mechanism of Github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue). This allows to validate the merged PR before pushing them to main. This is important to avoid parallel merge of PRs that would break the collection.
