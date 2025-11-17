from fastapi import APIRouter
from src.github.log_fetcher import fetch_logs
from src.llm.log_explainer import explain_logs
from src.models.logs import LogExplainRequest

router = APIRouter()

@router.post("/")
async def explain_log(payload: LogExplainRequest):
    logs = fetch_logs(payload.repo_url, payload.run_id)
    explanation = explain_logs(logs)
    return {"logs": logs[:2000], "explanation": explanation}
