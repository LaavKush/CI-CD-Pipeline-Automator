from fastapi import APIRouter
from src.models.workflow import WorkflowRequest
from src.analysis.analyzer_service import analyze_repository
from src.llm.ci_generator import generate_ci_yaml
from src.github.workflow_committer import commit_workflow
from src.pipeline.monitor import wait_for_workflow_run

router = APIRouter()

@router.post("/")
async def generate_workflow(payload: WorkflowRequest):

    # Step 1 — Analyze repo
    context = analyze_repository(payload.repo_url)

    # Step 2 — Generate YAML using LLM
    yaml_str = generate_ci_yaml(context)

    # Step 3 — Commit YAML to GitHub
    commit_info = commit_workflow(
        repo_url=payload.repo_url,
        branch=payload.branch,
        content=yaml_str
    )

    # Step 4 — Monitor CI run
    run_status = wait_for_workflow_run(
        repo_url=payload.repo_url,
        branch=payload.branch,
        commit_sha=commit_info["commit_sha"]
    )

    return {
        "status": "CI triggered",
        "run_status": run_status,
        "commit": commit_info
    }
