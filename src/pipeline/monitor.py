# src/pipeline/monitor.py
import time
import requests
from core.config import GITHUB_TOKEN, GITHUB_API_URL

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def get_latest_run(owner: str, repo: str, workflow_id: str = None):
    """
    Returns the latest run JSON for the repo (optionally filtered by workflow_id).
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    runs = data.get("workflow_runs", [])
    if not runs:
        return None
    if workflow_id:
        for run in runs:
            if run.get("workflow_id") == int(workflow_id) or run.get("name")==workflow_id:
                return run
    return runs[0]

def wait_for_run_completion(owner: str, repo: str, run_id: int, timeout: int = 600, poll_interval: int = 8):
    """
    Polls run status until completed or timeout.
    Returns run JSON once completed.
    """
    start = time.time()
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs/{run_id}"
    while True:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        run = r.json()
        status = run.get("status")   # queued | in_progress | completed
        conclusion = run.get("conclusion")  # success | failure | cancelled etc.
        if status == "completed":
            return run
        if time.time() - start > timeout:
            raise TimeoutError("Run did not complete within timeout")
        time.sleep(poll_interval)
