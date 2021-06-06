# Submit Pull Request

![eye_catch](./.github/img/eye_catch.png)

This is a GitHub Actions that will automatically submit a pull request.

## Functions

* Automatically create a pull request for a branch when you push a new branch related to an issue.
* Label the pull request the same as the issue.
* Add specific label(ex. WIP) in addition to the above.
* Add the information about the issue to the description of the pull request.
* Assigne the person who pushed commit

## Usage

Set up the GitHub Actions configuration file as follows.

```yaml
name: Submit Pull Request

on:
  create:

jobs:
  SubmitPullRequest:
    runs-on: ubuntu-latest
    steps:
      - name: Submit Pul Request
        uses: shimewtr/submit_pull_request@master
        env:
          GITHUB_ACCESS_TOKEN: ${{secrets.github_token}}
```

## Inputs

| Name                    | Description                                                                                                            | Required | Example                            | Default                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------        | ---------------------------------- |
| GITHUB_ACCESS_TOKEN     | Please enter an access token with permissions for this repository. In most cases, `${{secrets.github_token}}` is fine. | true     | `${{secrets.github_token}}`        |                                    |
| ASSIGN                  | If set to `true`, the person who pushed will be assigned to PR. (This is set to `true` by default.)                    | optional | `true` `false`                     | true                               |
| DRAFT                   | If set to `true`, the PR will be created in draft form.                                                                | optional | `true` `false`                     | false                              |
| LABEL                   | Label with the name you entered. The label should already be made.                                                     | optional | `WIP` `feature`                    |                                    |
| LABEL_SAME_AS_ISSUE     | If set to `true`, it will have the same label as the issue. (This is set to `true` by default.)                        | optional | `true` `false`                     | true                               |
| MILESTONE_SAME_AS_ISSUE | If set to `true`, it will have the same milestone as the issue. (This is set to `true` by default.)                    | optional | `true` `false`                     | true                               |
| TEMPLATE_FILE_PATH      | Specify the relative path to the PR template file.                                                                     | optional | `docs/pull_request_template.md`    | `.github/pull_request_template.md` |

## Template

Include a tag(`{submit_pull_request_issue_info}`) in the PR template file to replace it with the issue information.

```md
## Issue

{submit_pull_request_issue_info}
```

Replace the `{submit_pull_request_issue_info}` part with `refs #1 Issue title`

### Branch

The branch name must contain the issue's id.

ex. `1-fix-bug` `feature-23_file`
