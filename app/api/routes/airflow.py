from fastapi import APIRouter, status
from typing import Any, Optional
from app.api.controllers.airflow import publish_message_to_kafka
from app.settings.variables import (
    KAFKA_DAG_RUN_TOPIC_NAME,
    KAFKA_TASK_INSTANCE_TOPIC_NAME,
)

router = APIRouter()

@router.post("/events/dag_run", status_code=status.HTTP_200_OK,
             response_model=dict[str, Any])
async def publish_dag_run_state(
    dag_id: str,
    run_id: str,
    run_type: str,
    state: Optional[str] = None,
    queued_at: Optional[str] = None,
    execution_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    data_interval_start: Optional[str] = None,
    data_interval_end: Optional[str] = None,
    external_trigger: Optional[bool] = None,
    conf: Optional[str] = None,
    dag_hash_info: Optional[str] = None,
    msg: Optional[str] = None,
):
    payload = {
            "dag_id": dag_id,
            "run_id": run_id,
            "run_type": run_type,
            "state": state,
            "queued_at": queued_at,
            "execution_date": execution_date,
            "start_date": start_date,
            "end_date": end_date,
            "data_interval_start": data_interval_start,
            "data_interval_end": data_interval_end,
            "external_trigger": external_trigger,
            "conf": conf,
            "dag_hash_info": dag_hash_info,
            "msg": msg,
        }
    publish_message_to_kafka(
        topic=KAFKA_DAG_RUN_TOPIC_NAME,
        message=payload,
        key={"dag_id": dag_id}
    )
    return payload

@router.post("/events/task_instance", status_code=status.HTTP_200_OK
                , response_model=dict[str, Any])
async def publish_task_instance_state(
    dag_id: str,
    task_id: str,
    run_id: str,
    max_index: int,
    state: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    duration: Optional[float] = None,
    try_number: Optional[int] = None,
    hostname: Optional[str] = None,
    unixname: Optional[str] = None,
    job_id: Optional[str] = None,
    pool: Optional[str] = None,
    pool_slots: Optional[int] = None,
    queue: Optional[str] = None,
    priority_weight: Optional[int] = None,
    operator: Optional[str] = None,
    queued_by_job_id: Optional[str] = None,
    external_executor_id: Optional[str] = None,
):
    payload = {
            "dag_id": dag_id,
            "task_id": task_id,
            "run_id": run_id,
            "max_index": max_index,
            "state": state,
            "start_date": start_date,
            "end_date": end_date,
            "duration": duration,
            "try_number": try_number,
            "hostname": hostname,
            "unixname": unixname,
            "job_id": job_id,
            "pool": pool,
            "pool_slots": pool_slots,
            "queue": queue,
            "priority_weight": priority_weight,
            "operator": operator,
            "queued_by_job_id": queued_by_job_id,
            "external_executor_id": external_executor_id,
        }
    publish_message_to_kafka(
        topic=KAFKA_TASK_INSTANCE_TOPIC_NAME,
        message=payload,
        key={"dag_id": dag_id, "task_id": task_id}
    )    
    return payload