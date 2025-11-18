# # main.py
# import os
# from github_api.repo_manager import clone_repo, create_branch, commit_all_and_push
# from github_api.workflow_committer import create_or_update_file_api
# from pipeline.ci_runner import trigger_workflow_dispatch
# from pipeline.monitor import wait_for_run_completion, get_latest_run
# from github_api.log_fetcher import download_run_logs
# from core.config import CLONE_WORKDIR

# def run_workflow_for_repo(repo_url, branch_name="Github_Integration"):
#     # Clone
#     local_path = clone_repo(repo_url, force_clean=False)
#     # Option A: create branch locally & push
#     r = create_branch(local_path, branch_name)
#     # Suppose LLM produced 'yml_text' (for now use a sample)
#     yml_text = """name: CI\non: [push, workflow_dispatch]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Print Python\n        run: python --version\n"""
#     # Option B: add file via API directly
#     owner_repo = repo_url.rstrip('/').split('/')[-2:]
#     owner, repo = owner_repo
#     # For direct API create:
#     create_or_update_file_api(f"{owner}/{repo}", ".github/workflows/ci.yml", yml_text, "Add AI-generated workflow", branch=branch_name)
#     # Trigger run
#     trigger_workflow_dispatch(owner, repo, "ci.yml", ref=branch_name)
#     # Get latest run and wait
#     run = get_latest_run(owner, repo)
#     if not run:
#         print("No run detected")
#         return
#     run_id = run.get("id")
#     completed = wait_for_run_completion(owner, repo, run_id)
#     print("Completed:", completed.get("conclusion"))
#     if completed.get("conclusion") != "success":
#         logs_path = download_run_logs(owner, repo, run_id, dest_folder=os.path.join(CLONE_WORKDIR, "logs"))
#         print("Logs extracted to:", logs_path)

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 2:
#         print("Usage: python src/main.py <github_repo_url>")
#         sys.exit(1)
#     repo_url = sys.argv[1]
#     run_workflow_for_repo(repo_url)




# main.py

import os
import sys

# ------------------------------
# Ensure src/ is in python path
# ------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(CURRENT_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# ------------------------------
# Now real imports work
# ------------------------------
from github_api.repo_manager import clone_repo, create_branch, commit_all_and_push
from github_api.workflow_committer import create_or_update_file_api
from pipeline.ci_runner import trigger_workflow_dispatch
from pipeline.monitor import wait_for_run_completion, get_latest_run
from github_api.log_fetcher import download_run_logs
from core.config import CLONE_WORKDIR


def run_workflow_for_repo(repo_url, branch_name="Github_Integration"):
    print(f"🚀 Starting automation for repo: {repo_url}")

    # Clone repo
    local_path = clone_repo(repo_url, force_clean=False)

    # Create branch locally & push
    create_branch(local_path, branch_name)

    # Temporary workflow content
    yml_text = """name: CI
on: [push, workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Print Python
        run: python --version
"""

    # Extract owner/repo from URL
    owner, repo = repo_url.rstrip("/").split("/")[-2:]

    # Create workflow file using API
    create_or_update_file_api(
        f"{owner}/{repo}",
        ".github/workflows/ci.yml",
        yml_text,
        "Add AI-generated workflow",
        branch=branch_name,
    )

    # Trigger workflow dispatch
    trigger_workflow_dispatch(owner, repo, "ci.yml", ref=branch_name)

    # Get latest run
    run = get_latest_run(owner, repo)

    if not run:
        print("❌ No workflow run found after dispatch!")
        return

    run_id = run.get("id")
    print(f"⏳ Waiting for run {run_id} to complete...")

    completed = wait_for_run_completion(owner, repo, run_id)

    print("🏁 Completed with conclusion:", completed.get("conclusion"))

    # If failed, download logs
    if completed.get("conclusion") != "success":
        logs_path = download_run_logs(
            owner, repo, run_id,
            dest_folder=os.path.join(CLONE_WORKDIR, "logs")
        )
        print("📦 Logs extracted to:", logs_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <github_repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    run_workflow_for_repo(repo_url)
