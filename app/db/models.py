from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    game_id = Column(String, primary_key=True)
    job_id = Column(String, nullable=False)
    video_hash = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Integer, Text

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True)
    game_id = Column(String, nullable=False)

    status = Column(String, nullable=False, default="queued")  # queued|running|done|failed
    progress = Column(Integer, nullable=False, default=0)      # 0..100

    error = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
