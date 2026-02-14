from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, nullable=False)

    # ✅ 每筆 job 屬於某個 user
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
