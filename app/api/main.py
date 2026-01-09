from fastapi import FastAPI, UploadFile
import hashlib
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Basketball AI V1 running"}

@app.post("/upload")
async def upload_video(file: UploadFile):
    content = await file.read()
    video_hash = hashlib.sha256(content).hexdigest()

    return {
        "game_id": str(uuid.uuid4()),
        "job_id": str(uuid.uuid4()),
        "video_hash": video_hash,
        "filename": file.filename,
    }
