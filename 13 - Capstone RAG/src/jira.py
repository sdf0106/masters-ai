import os

from jira import JIRA


class Jira:
    def __init__(self):
        self.jira_config = {}
        self.jira = None

    def set_up(self, jira_config):
        jira_auth_token = os.getenv('JIRA_AUTH_TOKEN')
        self.jira_config = jira_config
        self.jira = JIRA(
            server=jira_config['jira_base_url'],
            basic_auth=("sdf0106@protonmail.com", jira_auth_token),
        )

    def create_jira_ticket(self, question):
        issue_details = {
            'project': self.jira_config['project_key'],
            'summary': f"{self.jira_config['ticket_summary_prefix']}: {question}",
            'description': f"Unable to find requested info in provided PDFs. Inquiry: '{question}'.",
            'issuetype': {'name': self.jira_config['issue_type']}
        }
        new_issue = self.jira.create_issue(fields=issue_details)
        return f"{self.jira_config['jira_base_url']}/browse/{new_issue.key}"
