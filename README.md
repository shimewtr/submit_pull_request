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

`.github/workflows/submit_pull_request.yml`

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
          LABEL: feature
```

`LABEL: feature` Labeling pull requests as "feature"(optional).

`.github/pull_request_template.md`

```
## Issue

{submit_pull_request_issue_info}

## Change
```

Replace `{submit_pull_request_issue_info}` with issue information.

ex. `refs #1 Issue title`

### Branch

The branch name must begin with the id of the issue.

ex. `1-fix-bug` `23_add_file`
