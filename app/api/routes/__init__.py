from fastapi import APIRouter
from app.api.routes.airflow import router as airflow_router

api_router = APIRouter()
api_router.include_router(airflow_router, prefix="/airflow", tags=["airflow"])