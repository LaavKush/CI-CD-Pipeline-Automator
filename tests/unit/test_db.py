from src.db.database import SessionLocal, engine
from src.db import models, schemas, crud

def test_create_history():
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)

    data = schemas.AnalysisCreate(
        repo_url="https://github.com/test",
        status="SUCCESS",
        log_text="No errors"
    )

    entry = crud.create_analysis(db, data)
    assert entry.id is not None
    assert entry.repo_url == "https://github.com/test"
