# src/github/repo_manager.py
import os
from git import Repo, GitCommandError
from core.config import CLONE_WORKDIR
from core.utils import remove_dir

def local_repo_path(owner: str, repo_name: str):
    return os.path.join(CLONE_WORKDIR, f"{owner}__{repo_name}")

def clone_repo(repo_url: str, force_clean: bool = False):
    """
    Clones repo_url into workspace/<owner>__<repo>
    returns local path
    """
    # repo_url example: https://github.com/owner/repo.git or git@github.com:owner/repo.git
    owner_repo = repo_url.rstrip("/").split("/")[-2:]
    owner, repo = owner_repo
    path = local_repo_path(owner, repo)
    if os.path.exists(path) and force_clean:
        remove_dir(path)
    if not os.path.exists(path):
        print("Cloning:", repo_url, "->", path)
        Repo.clone_from(repo_url, path)
    else:
        print("Repo already exists at", path)
    return path

def create_branch(local_path: str, branch_name: str, checkout: bool = True):
    r = Repo(local_path)

    # If branch exists, use it. Otherwise create it.
    if branch_name in r.branches:
        new_branch = r.branches[branch_name]
    else:
        new_branch = r.create_head(branch_name)

    # Checkout branch
    new_branch.checkout()

    # Push branch to GitHub
    origin = r.remotes.origin
    origin.push(f"{branch_name}:{branch_name}")

    print(f"✔️ Branch '{branch_name}' created and pushed to GitHub.")

    return r

def commit_all_and_push(local_path: str, commit_message: str, remote_name: str = "origin", branch_name: str = None):
    r = Repo(local_path)
    if branch_name is None:
        branch_name = r.active_branch.name
    r.git.add(all=True)
    r.index.commit(commit_message)
    origin = r.remote(name=remote_name)
    origin.push(refspec=f"{branch_name}:{branch_name}")
    return True
