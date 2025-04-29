from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from app.api.routes import api_router

logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()

APP_NAME = "Airflow Listener to Kafka"
DESCRIPTION = "API to send events from Airflow to Kafka's topic"

app = FastAPI(
    title=APP_NAME,
    description=DESCRIPTION,
    # redoc_url=None,
    # docs_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", status_code=200)
async def health():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")
