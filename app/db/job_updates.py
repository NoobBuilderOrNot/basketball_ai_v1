from datetime import datetime
from sqlalchemy import text
from app.db.database import SessionLocal

def set_job_status(job_id: str, status: str, progress: int | None = None, error: str | None = None):
    db = SessionLocal()
    params = {"job_id": job_id, "status": status, "updated_at": datetime.utcnow()}
    q = "UPDATE jobs SET status=:status, updated_at=:updated_at"

    if progress is not None:
        q += ", progress=:progress"
        params["progress"] = int(progress)

    if error is not None:
        q += ", error=:error"
        params["error"] = error

    q += " WHERE job_id=:job_id"
    db.execute(text(q), params)
    db.commit()
    db.close()
