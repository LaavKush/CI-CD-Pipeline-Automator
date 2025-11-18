# src/github_api/workflow_committer.py

import os
import base64
from github import Github, InputGitTreeElement  # correct PyGithub imports

from core.config import GITHUB_TOKEN, GITHUB_USER
from core.utils import safe_write_text

# Initialize Github client
gh = Github(GITHUB_TOKEN)


# ----------------------------------------------------------------------
# 1. Create or update file via GitHub API
# ----------------------------------------------------------------------
def create_or_update_file_api(repo_fullname: str, path: str, content: str, commit_message: str, branch: str = None):
    """
    Create or update a file via GitHub API.
    Automatically handles path creation such as .github/workflows/ci.yml.
    """
    repo = gh.get_repo(repo_fullname)
    target_branch = branch or repo.default_branch

    try:
        # Try to get existing file
        existing = repo.get_contents(path, ref=target_branch)

        # Update file
        repo.update_file(
            path,
            commit_message,
            content,
            existing.sha,
            branch=target_branch
        )
        return {"status": "updated"}

    except Exception:
        # File does not exist → create it
        repo.create_file(
            path,
            commit_message,
            content,
            branch=target_branch
        )
        return {"status": "created"}


# ----------------------------------------------------------------------
# 2. Local file writing + git committing + pushing
# ----------------------------------------------------------------------
def write_workflow_local_and_push(local_repo_path: str, yml_content: str, branch_name: str, commit_message: str):
    """
    Ensures workflow folder structure exists, writes ci.yml, commits, and pushes.
    Automatically creates:
        .github/
        .github/workflows/
        .github/workflows/ci.yml
    """
    from github_api.repo_manager import commit_all_and_push

    # Ensure directory structure exists
    github_dir = os.path.join(local_repo_path, ".github")
    workflows_dir = os.path.join(github_dir, "workflows")
    os.makedirs(workflows_dir, exist_ok=True)

    # File path for ci.yml
    workflow_file = os.path.join(workflows_dir, "ci.yml")

    # Write local file
    safe_write_text(workflow_file, yml_content)

    # Commit and push
    try:
        commit_all_and_push(local_repo_path, commit_message, branch_name=branch_name)
        print(f"[✔] Workflow committed & pushed to branch: {branch_name}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to push workflow: {e}")
        return False


# ----------------------------------------------------------------------
# 3. Helper: Write locally + push + create on GitHub if missing
# ----------------------------------------------------------------------
def ensure_workflow_and_push(local_repo_path: str, repo_fullname: str, branch_name: str):
    """
    High-level helper: creates default ci.yml if missing,
    writes locally, pushes, and syncs with GitHub.
    """

    DEFAULT_CI_YML = """name: CI
on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Show Python version
        run: python --version
"""

    workflow_rel_path = ".github/workflows/ci.yml"
    full_local_path = os.path.join(local_repo_path, workflow_rel_path)

    # Ensure folder structure exists
    os.makedirs(os.path.dirname(full_local_path), exist_ok=True)

    # Create file if missing
    if not os.path.exists(full_local_path):
        safe_write_text(full_local_path, DEFAULT_CI_YML)
        print("[✔] Created default ci.yml locally")

    # Push local changes
    write_workflow_local_and_push(
        local_repo_path=local_repo_path,
        yml_content=DEFAULT_CI_YML,
        branch_name=branch_name,
        commit_message="Add CI workflow"
    )

    # Sync to GitHub via API
    create_or_update_file_api(
        repo_fullname=repo_fullname,
        path=workflow_rel_path,
        content=DEFAULT_CI_YML,
        commit_message="Ensure CI workflow exists",
        branch=branch_name
    )

    print("[✔] CI workflow now exists locally and on GitHub.")
