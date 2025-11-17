# src/pipeline/ci_runner.py
import requests
from core.config import GITHUB_TOKEN, GITHUB_API_URL
from typing import Optional

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def trigger_workflow_dispatch(owner: str, repo: str, workflow_filename: str, ref: str = "main", inputs: Optional[dict] = None):
    """
    Trigger a workflow_dispatch event for a given workflow file name.
    workflow_filename e.g. 'ci.yml' or '.github/workflows/ci.yml' but recommended filename only.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/workflows/{workflow_filename}/dispatches"
    payload = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs
    r = requests.post(url, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.status_code == 204
