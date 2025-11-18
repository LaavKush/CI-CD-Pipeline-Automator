from sqlalchemy.orm import Session
from . import models, schemas

def create_analysis(db: Session, data: schemas.AnalysisCreate):
    entry = models.AnalysisHistory(
        repo_url=data.repo_url,
        status=data.status,
        log_text=data.log_text
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_all_history(db: Session):
    return db.query(models.AnalysisHistory).all()
