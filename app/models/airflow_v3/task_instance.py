from typing import Optional
from pydantic import Field
from app.models.base import AvroBase


class TaskInstance(AvroBase):
    dag_id: str = Field(
        ..., description="The unique identifier for the DAG.", example="my_example_dag"
    )
    task_id: str = Field(
        ...,
        description="The unique identifier for the task within the DAG.",
        example="process_data_task",
    )
    run_id: str = Field(
        ...,
        description="The unique identifier for the DAG run this task instance belongs to.",
        example="manual__2023-10-27T10:00:00+00:00",
    )
    map_index: int = Field(  # Renamed from map_index in original if that was the intent
        ...,
        description="The map index if the task is dynamically mapped. Often -1 for non-mapped tasks.",
        example=-1,  # Example: 0 for the first mapped task, -1 if not mapped
    )
    state: Optional[str] = Field(
        None,
        description="The current state of the task instance (e.g., 'queued', 'running', 'success', 'failed', 'skipped').",
        example="success",
    )
    start_date: Optional[str] = Field(
        None,
        description="Timestamp when the task instance started execution (ISO 8601 format).",
        example="2023-10-27T10:01:00.111111+00:00",
    )
    end_date: Optional[str] = Field(
        None,
        description="Timestamp when the task instance finished execution (ISO 8601 format).",
        example="2023-10-27T10:02:30.222222+00:00",
    )
    duration: Optional[float] = Field(
        None,
        description="Duration of the task instance execution in seconds.",
        example=90.111,
    )
    try_number: Optional[int] = Field(
        None,
        description="The attempt number for this task instance execution (1-based).",
        example=1,
    )
    hostname: Optional[str] = Field(
        None,
        description="Hostname of the worker that executed the task instance.",
        example="worker-hostname-123.example.com",
    )
    unixname: Optional[str] = Field(
        None, description="Unix username running the task instance.", example="airflow"
    )
    job_id: Optional[str] = Field(
        None,
        description="Identifier for the job associated with this task instance (e.g., LocalTaskJob ID).",
        example="12345",
    )
    pool: Optional[str] = Field(
        None,
        description="The pool assigned to the task instance.",
        example="default_pool",
    )
    pool_slots: Optional[int] = Field(
        None,
        description="Number of pool slots occupied by the task instance.",
        example=1,
    )
    queue: Optional[str] = Field(
        None,
        description="The queue assigned to the task instance (relevant for CeleryExecutor, etc.).",
        example="default",
    )
    priority_weight: Optional[int] = Field(
        None, description="Priority weight assigned to the task instance.", example=1
    )
    operator: Optional[str] = Field(
        None,
        description="The class name of the Airflow operator used by the task.",
        example="BashOperator",
    )
    queued_by_job_id: Optional[str] = Field(
        None,
        description="Identifier for the scheduler job that queued this task instance.",
        example="67890",
    )
    external_executor_id: Optional[str] = Field(
        None,
        description="Identifier used by external executors (e.g., Kubernetes pod name).",
        example="my-dag-my-task-pod-xyz123",
    )

    class Config:
        # Add example for the whole model in docs
        json_schema_extra = {
            "example": {
                "dag_id": "my_processing_dag",
                "task_id": "transform_data",
                "run_id": "scheduled__2023-10-26T00:00:00+00:00",
                "map_index": -1,
                "state": "success",
                "start_date": "2023-10-26T01:05:15.123456+00:00",
                "end_date": "2023-10-26T01:07:45.654321+00:00",
                "duration": 150.531,
                "try_number": 1,
                "hostname": "airflow-worker-abc",
                "unixname": "airflow",
                "job_id": "54321",
                "pool": "data_processing_pool",
                "pool_slots": 1,
                "queue": "processing",
                "priority_weight": 10,
                "operator": "PythonOperator",
                "queued_by_job_id": "98765",
                "external_executor_id": None,
            }
        }
