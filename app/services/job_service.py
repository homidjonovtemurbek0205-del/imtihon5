from fastapi import HTTPException
from sqlalchemy import delete, select, or_
from sqlalchemy.orm import Session

from app.db.models import JobPost
from app.schemas.auth_schemas import CurrentUser
from app.schemas.job_schemas import JobPostSchema


def create_job(data: JobPostSchema, current_user: CurrentUser, db: Session):
    job_data = data.model_dump()
    job_data["owner_id"] = current_user.id
    job_post = JobPost(**job_data)
    db.add(job_post)
    db.commit()
    db.refresh(job_post)
    return job_post


def get_all_jobs(db: Session):
    jobs = db.execute(select(JobPost)).scalars().all()
    return jobs


def search_jobs(query: str, db: Session):
    search_filter = or_(
        JobPost.title.ilike(f"%{query}%"),
        JobPost.description.ilike(f"%{query}%")
    )
    jobs = db.execute(select(JobPost).where(search_filter)).scalars().all()
    return jobs


def get_my_jobs(current_user: CurrentUser, db: Session):
    jobs = db.execute(select(JobPost).where(JobPost.owner_id == current_user.id)).scalars().all()
    return jobs


def get_job_by_id(job_id: int, db: Session):
    job = db.execute(select(JobPost).where(JobPost.id == job_id)).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job post not found")
    return job


def update_job(job_id: int, data: JobPostSchema, current_user: CurrentUser, db: Session):
    job = db.execute(select(JobPost).where(JobPost.id == job_id)).scalar_one_or_none()

    if job is None:
        raise HTTPException(status_code=404, detail="Job post not found")

    if job.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    job.title = data.title
    job.description = data.description
    job.salary = data.salary

    db.commit()
    db.refresh(job)
    return job


def delete_job(job_id: int, current_user: CurrentUser, db: Session):
    job = db.execute(select(JobPost).where(JobPost.id == job_id)).scalar_one_or_none()

    if job is None:
        raise HTTPException(status_code=404, detail="Job post not found")

    if job.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.execute(delete(JobPost).where(JobPost.id == job_id))
    db.commit()
    return job