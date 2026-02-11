from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from database import SessionLocal, engine
from models import Base
from schemas import JobCreate, JobResponse, JobUpdate
import crud

# Create tables (first run will create jobs.db)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}

@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job_id=str(uuid4()), job=job)

@app.get("/jobs", response_model=List[JobResponse])
def list_jobs(
    status: Optional[str] = Query(default=None, description="Filter by status"),
    db: Session = Depends(get_db),
):
    return crud.get_jobs(db, status=status)

@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: str, update: JobUpdate, db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.update_job_status(db, job, update)

@app.delete("/jobs/{job_id}")
def remove_job(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    crud.delete_job(db, job)
    return {"message": "Job deleted"}
