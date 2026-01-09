import time
from app.db.database import SessionLocal
from sqlalchemy import text

def process_game(game_id: str):
    # placeholder job (V1): simulate work
    time.sleep(2)

    # later: this is where we will run detection + tracking + ref logic
    db = SessionLocal()
    # for now we just mark that processing happened by updating filename (tiny proof)
    db.execute(text("UPDATE games SET filename = filename WHERE game_id = :gid"), {"gid": game_id})
    db.commit()
    db.close()

    return {"status": "processed", "game_id": game_id}
