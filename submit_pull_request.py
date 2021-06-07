import base64
import os
import re
import json
from github import Github

GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
GITHUB_REF = os.environ['GITHUB_REF']
GITHUB_REPOSITORY = os.environ['GITHUB_REPOSITORY']
GITHUB_ACTOR = os.environ['GITHUB_ACTOR']

ASSIGN = os.environ['ASSIGN'].lower() == "true" if "ASSIGN" in os.environ else True
DEBUG = os.environ['DEBUG'].lower() == "true" if "DEBUG" in os.environ else False
DRAFT = os.environ['DRAFT'].lower() == "true" if "DRAFT" in os.environ else False
LABEL = [x.strip() for x in os.environ['LABEL'].split(',')] if "LABEL" in os.environ else []
LABEL_SAME_AS_ISSUE = os.environ['LABEL_SAME_AS_ISSUE'].lower() == "true" if "LABEL_SAME_AS_ISSUE" in os.environ else True
MILESTONE_SAME_AS_ISSUE = os.environ['MILESTONE_SAME_AS_ISSUE'].lower() == "true" if "MILESTONE_SAME_AS_ISSUE" in os.environ else True
TEMPLATE_FILE_PATH = os.environ['TEMPLATE_FILE_PATH'] if "TEMPLATE_FILE_PATH" in os.environ else ".github/pull_request_template.md"
AUTHORS = os.environ['AUTHORS'] if "AUTHORS" in os.environ else "{}"

class SubmitPullRequest():
    def __init__(self):
        self.branch_id = self.parse_branch_name()
        self.repo = Github(self.get_access_token()).get_repo(GITHUB_REPOSITORY)
        self.issue = self.get_issue()
        self.pr_body = self.build_pr_body()
        self.pr = self.create_pull_request()
        self.add_label_to_pull_request()
        self.add_milestone_to_pull_request()
        self.add_assignees_to_pull_request()

    def add_assignees_to_pull_request(self):
        try:
            if ASSIGN:
                self.pr.add_to_assignees(GITHUB_ACTOR)
        except:
            self.error_handler("Failed to add assignees to pull request")

    def add_label_to_pull_request(self):
        try:
            if LABEL_SAME_AS_ISSUE:
                for label in self.issue.labels:
                    self.pr.add_to_labels(label.name)
            for label in (set(LABEL) & set([x.name for x in self.repo.get_labels()])):
                self.pr.add_to_labels(label)
        except:
            self.error_handler("Failed to add label to pull request")

    def add_milestone_to_pull_request(self):
        try:
            if MILESTONE_SAME_AS_ISSUE:
                self.repo.get_issue(self.pr.number).edit(milestone=self.issue.milestone)
        except:
            self.error_handler("Failed to add milestone to pull request")

    def build_pr_body(self):
        template_content = self.get_template_content()
        return self.replace_tag_to_issue_information(template_content)

    def create_pull_request(self):
        try:
            issue_number = self.issue.number
            title = self.issue.title
            pr_title = "ref #{} {}".format(issue_number, title)
            pr = self.repo.create_pull(
                title=pr_title,
                body=self.pr_body,
                head=GITHUB_REF,
                base=self.repo.default_branch,
                draft=DRAFT)
            return pr
        except:
            self.error_handler("Failed to create pull request")

    def error_handler(self, message):
        print('\033[31m' + message + '\033[0m')
        raise Exception

    def get_issue(self):
        try:
            issue = self.repo.get_issue(self.branch_id)
        except:
            if DEBUG:
                issue = IssueMock()
            else:
                self.error_handler("Failed to get the issue")
        if issue:
            return issue
        else:
            self.error_handler("No corresponding issue")

    def get_template_content(self):
        try:
            contents = self.repo.get_contents(TEMPLATE_FILE_PATH)
            contents = base64.b64decode(contents.content).decode('utf8', 'ignore')
            return contents
        except:
            return ''

    def parse_branch_name(self):
        m = re.findall(r'/\d+', GITHUB_REF)
        try:
            branch_id = int(m[-1][1:])
            return branch_id
        except:
            self.error_handler("Branch name is incorrect")

    def replace_tag_to_issue_information(self, content):
        if '{submit_pull_request_issue_info}' in content:
            issue_number = self.issue.number
            title = self.issue.title
            issue_info = "ref #{} {}\n".format(issue_number, title)
            return content.format(submit_pull_request_issue_info=issue_info)
        else:
            return content

    def get_access_token(self):
        try:
            authors_json = json.loads(AUTHORS)
            for author in authors_json.get("authors"):
                if author.get("name") == GITHUB_ACTOR:
                    return author.get("token")
        except:
            pass
        return GITHUB_ACCESS_TOKEN

class IssueMock:
    number = 0
    title = 'temporary title'
    labels = []
    milestone = ''


if __name__ == '__main__':
    SubmitPullRequest()
