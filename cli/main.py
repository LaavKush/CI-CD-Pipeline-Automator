import typer
from src.db.database import SessionLocal, engine
from src.db import models, schemas, crud

app = typer.Typer()

# Ensure DB tables exist
models.Base.metadata.create_all(bind=engine)

@app.command()
def save(repo: str, status: str, log: str):
    """
    Save an analysis entry into DB.
    """
    db = SessionLocal()
    data = schemas.AnalysisCreate(repo_url=repo, status=status, log_text=log)
    result = crud.create_analysis(db, data)
    typer.echo(f"Saved entry ID: {result.id}")

@app.command()
def history():
    """
    Show previous analysis history.
    """
    db = SessionLocal()
    entries = crud.get_all_history(db)
    for e in entries:
        typer.echo(f"{e.id} | {e.repo_url} | {e.status}")

if __name__ == "__main__":
    app()
