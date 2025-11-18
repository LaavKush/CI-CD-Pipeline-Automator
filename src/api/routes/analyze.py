from fastapi import APIRouter
from src.models.analyze import AnalyzeRequest, AnalyzeResponse
from src.analysis.analyzer_service import summarize_repo

router = APIRouter()

@router.post("/", response_model=AnalyzeResponse)
async def analyze_repo(payload: AnalyzeRequest):
    summary = summarize_repo(payload.repo_url)

    return AnalyzeResponse(
        language="unknown",
        framework=None,
        test_runner=None,
        hasDockerfile=False,
        context_json=summary
    )
