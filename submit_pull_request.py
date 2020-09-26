import base64
import json
import os
import re
import requests
import sys
import textwrap
import urllib
from github import Github

GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
GITHUB_REF = os.environ['GITHUB_REF']
GITHUB_REPOSITORY = os.environ['GITHUB_REPOSITORY']
GITHUB_ACTOR = os.environ['GITHUB_ACTOR']


def main():
    branch_id = get_branch_id()
    repo = Github(GITHUB_ACCESS_TOKEN).get_repo(GITHUB_REPOSITORY)
    issue = get_issue(repo, branch_id)
    template_content = get_template_content(repo, issue)
    create_pull_request(repo, template_content, issue)


def create_pull_request(repo, template_content, issue):
    pr = repo.create_pull(title="refs #{id} {issue_title}".format(id=issue.number, issue_title=issue.title),
                          body=template_content,
                          head=GITHUB_REF,
                          base=repo.default_branch)
    for label in issue.labels:
        pr.add_to_labels(label.name)
    if any(label.name == "WIP" for label in repo.get_labels()):
        pr.add_to_labels("WIP")
    pr.add_to_assignees(GITHUB_ACTOR)


def error_handler(message):
    print(message)
    sys.exit()


def get_branch_id():
    m = re.findall(r'/\d+', GITHUB_REF)
    if m:
        return int(m[-1][1:])
    else:
        error_handler("Branch name is incorrect")


def get_issue(repo, id):
    issue = repo.get_issue(id)
    if issue:
        return issue
    else:
        error_handler("No corresponding issue")


def get_template_content(repo, issue):
    contents = repo.get_contents(".github/pull_request_template.md")
    contents = base64.b64decode(contents.content).decode('utf8', 'ignore')
    return contents.format(issue_number=issue.number, title=issue.title)


if __name__ == '__main__':
    main()
