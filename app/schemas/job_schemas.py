from decimal import Decimal
from pydantic import BaseModel

class JobPostSchema(BaseModel):
    title: str
    description: str
    salary: Decimal

class JobPostResponse(BaseModel):
    id: int
    title: str
    description: str
    salary: Decimal

class JobPostListResponse(BaseModel):
    id: int
    title: str
    salary: Decimal

class JobPostDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    salary: Decimal
    owner_id: int

class JobPostSearchResponse(BaseModel):
    id: int
    title: str

class JobPostMyJobsResponse(BaseModel):
    id: int
    title: str

class JobPostUpdateResponse(BaseModel):
    id: int
    title: str
    salary: Decimal