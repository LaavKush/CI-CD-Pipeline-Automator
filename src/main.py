from fastapi import FastAPI
from src.api.routes import analyze, workflow, logs, fix

app = FastAPI(title="AI-Driven CI/CD Automator", version="1.0.0")

app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
app.include_router(workflow.router, prefix="/workflow", tags=["Workflow"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(fix.router, prefix="/fix", tags=["Fix (Optional)"])

@app.get("/")
def root():
    return {"message": "CI/CD Automator Backend Running 🚀"}
