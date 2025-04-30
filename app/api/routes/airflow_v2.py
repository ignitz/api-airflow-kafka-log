from typing import Any
from fastapi import APIRouter, status
from app.api.controllers.common import publish_message_to_kafka
from app.settings.variables import (
    KAFKA_AIRFLOW_V2_DAG_RUN_TOPIC_NAME,
    KAFKA_AIRFLOW_V2_TASK_INSTANCE_TOPIC_NAME,
)
from app.models.airflow_v2.dag_run import DagRun
from app.models.airflow_v2.task_instance import TaskInstance

AIRLFOW_MAJOR_VERSION = "v2"

router = APIRouter()


@router.post(
    "/events/dag_run", status_code=status.HTTP_200_OK, response_model=dict[str, Any]
)
async def publish_dag_run_state(dag_run: DagRun):
    payload = dag_run.model_dump()
    dag_id = payload["dag_id"]
    publish_message_to_kafka(
        topic=KAFKA_AIRFLOW_V2_DAG_RUN_TOPIC_NAME,
        version=AIRLFOW_MAJOR_VERSION,
        message=payload,
        key={"dag_id": dag_id},
    )
    return dag_run.model_dump()


@router.post(
    "/events/task_instance",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
async def publish_task_instance_state(task_instance: TaskInstance):
    payload = task_instance.model_dump()
    dag_id = payload["dag_id"]
    task_id = payload["task_id"]
    publish_message_to_kafka(
        topic=KAFKA_AIRFLOW_V2_TASK_INSTANCE_TOPIC_NAME,
        version=AIRLFOW_MAJOR_VERSION,
        message=payload,
        key={"dag_id": dag_id, "task_id": task_id},
    )
    return payload
