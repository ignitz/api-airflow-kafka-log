#!/bin/bash

NUM_WORKERS=$(nproc --all)

gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --workers ${NUM_WORKERS} --bind 0.0.0.0:8000
