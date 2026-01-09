from fastapi import FastAPI, UploadFile
import hashlib
import uuid

from rq import Queue
import redis

from app.db.database import engine, SessionLocal
from app.db.models import Base, Game, Job
from workers.jobs import process_game

app = FastAPI()
Base.metadata.create_all(bind=engine)

redis_conn = redis.Redis(host="redis", port=6379)
q = Queue("default", connection=redis_conn)

@app.get("/")
def root():
    return {"status": "Basketball AI V1 running"}

@app.post("/upload")
async def upload_video(file: UploadFile):
    content = await file.read()
    video_hash = hashlib.sha256(content).hexdigest()

    game_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    db = SessionLocal()

    db.add(Game(
        game_id=game_id,
        job_id=job_id,
        video_hash=video_hash,
        filename=file.filename,
    ))

    db.add(Job(
        job_id=job_id,
        game_id=game_id,
        status="queued",
        progress=0,
        error=None,
    ))

    db.commit()
    db.close()

    rq_job = q.enqueue(process_game, game_id, job_id)

    return {
        "game_id": game_id,
        "job_id": job_id,
        "rq_job_id": rq_job.id,
        "filename": file.filename,
    }

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.job_id == job_id).first()
    db.close()

    if not job:
        return {"error": "job_not_found", "job_id": job_id}

    return {
        "job_id": job.job_id,
        "game_id": job.game_id,
        "status": job.status,
        "progress": job.progress,
        "error": job.error,
        "updated_at": str(job.updated_at),
    }
