import time
from app.db.job_updates import set_job_status

def process_game(game_id: str, job_id: str):
    # Mark running
    set_job_status(job_id, "running", progress=1)

    try:
        # Placeholder pipeline steps (we’ll replace later with real video work)
        set_job_status(job_id, "running", progress=10)
        time.sleep(1)

        set_job_status(job_id, "running", progress=40)
        time.sleep(1)

        set_job_status(job_id, "running", progress=70)
        time.sleep(1)

        set_job_status(job_id, "done", progress=100)
        return {"status": "processed", "game_id": game_id, "job_id": job_id}

    except Exception as e:
        set_job_status(job_id, "failed", progress=100, error=str(e))
        raise
