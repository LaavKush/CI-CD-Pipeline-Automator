# src/github/log_fetcher.py
import requests, os, io
from core.config import GITHUB_TOKEN, GITHUB_API_URL
from core.utils import extract_zip

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def download_run_logs(owner: str, repo: str, run_id: int, dest_folder: str):
    """
    Downloads logs ZIP for a workflow run and extracts it into dest_folder/run_<id>/
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
    with requests.get(url, headers=HEADERS, stream=True) as r:
        r.raise_for_status()
        # GitHub returns a redirect to the actual zip url; requests follows it.
        data = io.BytesIO(r.content)
        zip_path = os.path.join(dest_folder, f"run_{run_id}.zip")
        os.makedirs(dest_folder, exist_ok=True)
        with open(zip_path, "wb") as f:
            f.write(data.getvalue())
    extract_dir = os.path.join(dest_folder, f"run_{run_id}")
    extract_zip(zip_path, extract_dir)
    return extract_dir
