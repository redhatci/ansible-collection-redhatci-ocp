# Create PR Role
This role groups the common tasks to create the GitHub Pull Request needed for the certification workflows.
For now, it is used by the `chart_verifier` and `preflight` roles, to handle respectively helm chart certification and operator bundle certification.

Name                                | Default   | Required                    | Description
----------------------------------- |-----------|-----------------------------| -------------------------------------------------------------
product_name                        | undefined | true                        | Name of the chart or the operator you want to certify.
product_version                     | undefined | true                        | Version of the product.
work_dir                            | /tmp      | false                       | Directory to store the tests results.
github_token_path                   | undefined | true                        | GitHub token to be used to push the chart and the results to a repository.
partner_name                        | undefined | true/false                  | Define this parameter only when opening PR for chart_verifier. Partner name to be used in the pull request title.
partner_email                       | undefined | true/false                  | Define this parameter only when opening PR for chart_verifier. Email address to be used in the pull request.
target_repository                   | undefined | true                        | GitHub repository where the pull request will be created.
product_type                        | undefined | true                        | Product type. Either "helmchart" or "operator".

Those are the common variables used by both certification project.
It includes tasks to generate an SSH key needed to push to GitHub repository and add it to the GitHub account.
Specially, it generates an ed25519 key into the '.ssh/' folder of the Ansible user's HOME and, in order to not taint any configuration, it is doing a backup of the already existing SSH key (if it already exists).

## Operator Bundle certification
Check the [README](roles/preflight/README.md) of the 'preflight' role for more details.

After check tests have been executed in the preflight role on the operator, the role can be called to create a PR which is needed in the certification workflow of an operator.
The role will create a fork of the 'certified-operators' project, then add the manifests extracted from the bundle operator image and add a ci.yaml configuration file. The changes are committed and finally create a PR to be added in the catalog of certified operator.

Requirements:
    - If you create a cert project manually, please think to add GitHub user into connect.redhat.com -> Operator Bundle Image. If you chose an automated project creation, that will be done for you.
    - Please precise on which OCP you tested the operator as `com.redhat.openshift.versions: "v4.7-v4.10"` in /medatadata/annotations.yaml of your bundle image.

## Helm chart certification
Check the [README](roles/chart_verifier/README.md) of the 'chart_verifier' role.

