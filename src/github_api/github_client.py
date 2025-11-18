# src/github/github_client.py
from github import Github

from core.config import GITHUB_TOKEN, GITHUB_API_URL, GITHUB_USER

if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN missing in environment")

# PyGithub client
gh = Github(GITHUB_TOKEN)

def get_repo(full_name: str):
    """
    full_name: 'owner/repo'
    """
    return gh.get_repo(full_name)

def create_pull_request(repo, title: str, body: str, head: str, base: str = "main"):
    """
    Creates a PR from head -> base
    repo: PyGithub Repository object
    head: branch name like "github_integration_fix"
    """
    return repo.create_pull(title=title, body=body, head=head, base=base)
