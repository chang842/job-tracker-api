from sqlalchemy.orm import Session
from models import Job
from schemas import JobCreate, JobUpdate

def create_job(db: Session, job_id: str, job: JobCreate) -> Job:
    new_job = Job(
        id=job_id,
        company=job.company,
        position=job.position,
        status=job.status,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def get_jobs(db: Session, status: str | None = None) -> list[Job]:
    q = db.query(Job)
    if status:
        q = q.filter(Job.status == status)
    return q.all()

def get_job_by_id(db: Session, job_id: str) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()

def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()

def update_job_status(db: Session, job: Job, update: JobUpdate) -> Job:
    job.status = update.status
    db.commit()
    db.refresh(job)
    return job
