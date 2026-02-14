from sqlalchemy.orm import Session
from models import Job, User
from schemas import JobCreate, JobUpdate


# ---------- Users ----------
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_id: str, email: str, password_hash: str) -> User:
    user = User(id=user_id, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Jobs ----------
def create_job(db: Session, job_id: str, user_id: str, job: JobCreate) -> Job:
    new_job = Job(
        id=job_id,
        user_id=user_id,
        company=job.company,
        position=job.position,
        status=job.status,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


def get_jobs(db: Session, user_id: str, status: str | None = None) -> list[Job]:
    q = db.query(Job).filter(Job.user_id == user_id)
    if status:
        q = q.filter(Job.status == status)
    return q.order_by(Job.created_at.desc()).all()


def get_job_by_id(db: Session, user_id: str, job_id: str) -> Job | None:
    return db.query(Job).filter(Job.user_id == user_id, Job.id == job_id).first()


def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()


def update_job_status(db: Session, job: Job, update: JobUpdate) -> Job:
    job.status = update.status
    db.commit()
    db.refresh(job)
    return job
