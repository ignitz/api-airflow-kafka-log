from fastapi import APIRouter
from app.api.routes.airflow_v2 import router as airflow_router_2
from app.api.routes.airflow_v3 import router as airflow_router_3

api_router = APIRouter()
api_router.include_router(airflow_router_2, prefix="/airflow_v2", tags=["airflow"])
api_router.include_router(airflow_router_3, prefix="/airflow_v3", tags=["airflow"])
