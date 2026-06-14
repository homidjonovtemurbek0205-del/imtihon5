from fastapi import APIRouter, Depends, Query

from app.dependencies.auth_dependencies import get_current_user
from app.dependencies.db_dependencies import get_db
from app.schemas.auth_schemas import CurrentUser
from app.schemas.job_schemas import JobPostSchema, JobPostResponse, JobPostListResponse, JobPostDetailResponse, JobPostSearchResponse, JobPostMyJobsResponse, JobPostUpdateResponse
from app.services import job_service

router = APIRouter()


@router.post("/jobs", response_model=JobPostResponse)
def create_job(data: JobPostSchema, current_user: CurrentUser = Depends(get_current_user), db=Depends(get_db),):
    return job_service.create_job(data, current_user, db)


@router.get("/jobs", response_model=list[JobPostListResponse])
def get_all_jobs(db=Depends(get_db)):
    return job_service.get_all_jobs(db)


@router.get("/jobs/search", response_model=list[JobPostSearchResponse])
def search_jobs(query: str, db=Depends(get_db)):
    return job_service.search_jobs(query, db)


@router.get("/my-jobs", response_model=list[JobPostMyJobsResponse])
def get_my_jobs(current_user: CurrentUser = Depends(get_current_user), db=Depends(get_db)):
    return job_service.get_my_jobs(current_user, db)


@router.get("/jobs/{job_id}", response_model=JobPostDetailResponse)
def get_job_by_id(job_id: int, db=Depends(get_db)):
    return job_service.get_job_by_id(job_id, db)


@router.put("/jobs/{job_id}", response_model=JobPostUpdateResponse)
def update_job(job_id: int, data: JobPostSchema, current_user: CurrentUser = Depends(get_current_user), db=Depends(get_db)):
    return job_service.update_job(job_id, data, current_user, db)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, current_user: CurrentUser = Depends(get_current_user), db=Depends(get_db)):
    job_service.delete_job(job_id, current_user, db)
    return {"message": "E'lon muvaffaqiyatli o'chirildi"}