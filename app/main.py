from fastapi import FastAPI
from app.db.base import engine, Base
from app.routers.auth_router import router as auth_router
from app.routers.job_router import router as job_router


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth_router)
app.include_router(job_router)