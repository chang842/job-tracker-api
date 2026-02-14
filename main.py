from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from database import SessionLocal, engine, get_db
from models import Base, User

from auth import router as auth_router
app = FastAPI()
app.include_router(auth_router)

import crud
from schemas import (
    JobCreate,
    JobResponse,
    JobUpdate,
    UserRegister,
    UserPublic,
    TokenResponse,
)
from auth import hash_password, verify_password, create_access_token, decode_access_token, authenticate_user

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}


# ---------------- Auth ----------------
@app.post("/auth/register", response_model=UserPublic)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = crud.create_user(
        db=db,
        user_id=str(uuid4()),
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    return user


@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------------- Jobs (Protected) ----------------
@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.create_job(db, job_id=str(uuid4()), user_id=current_user.id, job=job)


@app.get("/jobs", response_model=List[JobResponse])
def list_jobs(
    status: Optional[str] = Query(default=None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.get_jobs(db, user_id=current_user.id, status=status)


@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: str, update: JobUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    job = crud.get_job_by_id(db, user_id=current_user.id, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.update_job_status(db, job, update)


@app.delete("/jobs/{job_id}")
def remove_job(job_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    job = crud.get_job_by_id(db, user_id=current_user.id, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    crud.delete_job(db, job)
    return {"message": "Job deleted"}
