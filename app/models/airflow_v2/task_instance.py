import datetime
from typing import Dict, Any
from typing import Optional
from pydantic import Field
from app.models.base import AvroBase


class TaskInstance(AvroBase):
    dag_id: str = Field(
        ...,
        description="The unique identifier for the DAG.",
        examples=["my_dag"]
    )
    task_id: str = Field(
        ...,
        description="The unique identifier for the Task within the DAG.",
        examples=["process_data"]
    )
    run_id: str = Field(
        ...,
        description="The unique identifier for the specific DAG run.",
        examples=["manual__2025-04-30T15:40:00+00:00"]
    )
    map_index: int = Field(
        ...,
        description="The map index for mapped tasks. -1 for non-mapped tasks.",
        examples=[-1, 0, 1]
    )

    # --- Execution Details ---
    start_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the task instance execution actually started.",
        examples=["2025-04-30T15:40:05.123456+00:00", None]
    )
    end_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the task instance execution finished.",
        examples=["2025-04-30T15:45:10.987654+00:00", None]
    )
    duration: Optional[float] = Field(
        None,
        description="Duration of the task instance execution in seconds.",
        examples=[305.8642, None]
    )
    state: Optional[str] = Field( # Or use TaskInstanceState Enum for stricter validation
        None,
        description="The current state of the task instance.",
        examples=["success", "running", "failed", None]
    )
    try_number: int = Field(
        ...,
        description="The current try number for this task instance execution.",
        examples=[1, 2]
    )
    max_tries: Optional[int] = Field( # Often derived from task, but useful context
         None,
         description="The maximum number of retries allowed for the task.",
         examples=[3, 0, None] # None might mean default or unlimited based on context
    )
    hostname: Optional[str] = Field( # Marked Optional as it might not always be set
        None,
        description="Hostname of the worker that executed the task instance.",
        examples=["worker-hostname-123", None]
    )
    unixname: Optional[str] = Field( # Marked Optional
        None,
        description="Unix username running the task instance.",
        examples=["airflow", None]
    )
    job_id: Optional[int] = Field(
        None,
        description="The ID of the Airflow Job that executed this task instance (e.g., LocalTaskJob ID).",
        examples=[101, None]
    )
    pid: Optional[int] = Field(
        None,
        description="The process ID (PID) of the worker process that executed the task.",
        examples=[12345, None]
    )
    operator: Optional[str] = Field(
        None,
        description="The class name of the operator used for this task instance.",
        examples=["BashOperator", "PythonOperator", None]
    )
    executor_config: str = Field(
        default_factory="{}",
        description="Executor-specific configuration dictionary.",
        examples=[{"KubernetesExecutor": {"image": "custom-image:latest"}}, {}]
    )
    external_executor_id: Optional[str] = Field(
        None,
        description="Identifier used by external executors (like Celery task ID).",
        examples=["celery-task-uuid-...", None]
    )

    # --- Scheduling Details ---
    pool: str = Field(
        ...,
        description="The pool assigned to this task instance.",
        examples=["default_pool", "high_memory_pool"]
    )
    pool_slots: int = Field(
        ...,
        description="The number of pool slots occupied by this task instance.",
        examples=[1]
    )
    queue: str = Field(
        ...,
        description="The queue assigned to this task instance.",
        examples=["default", "gpu_queue"]
    )
    priority_weight: int = Field(
        ...,
        description="Priority weight of the task instance.",
        examples=[1, 10]
    )
    queued_by_job_id: Optional[int] = Field(
        None,
        description="The ID of the SchedulerJob that queued this task instance.",
        examples=[55, None]
    )
    queued_dttm: Optional[datetime.datetime] = Field( # Alias for queued_when in some contexts
        None,
        description="Timestamp when the task instance was queued.",
        alias="queued_when", # Common alias
        validation_alias="queued_when", # For input validation
        examples=["2025-04-30T15:39:55.123+00:00", None]
    )

    # --- Trigger/Deferral Details ---
    trigger_id: Optional[int] = Field(
        None,
        description="The ID of the Trigger associated with this task instance if deferred.",
        examples=[20, None]
    )
    trigger_timeout: Optional[float] = Field( # Represent timedelta as seconds
        None,
        description="Timeout duration for the trigger in seconds.",
        examples=[3600.0, None]
    )
    next_method: Optional[str] = Field(
        None,
        description="The method to call when the trigger fires.",
        examples=["execute_complete", None]
    )
    next_kwargs: Optional[Dict[str, Any]] = Field(
        None,
        description="Keyword arguments to pass to the next_method.",
        examples=[{"event": {"status": "ready"}}, None]
    )

    # --- Metadata ---
    updated_at: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when this task instance record was last updated.",
        examples=["2025-04-30T15:45:11.123456+00:00", None]
    )
    rendered_map_index: Optional[int] = Field(
        None,
        description="The map index rendered in the templated fields.",
        examples=[0, 1, None]
    )
    is_trigger_log_event: Optional[bool] = Field(
        None,
        description="Indicates if the log event is related to a trigger.",
        examples=[False, True, None]
    )
    task_display_name: Optional[str] = Field(
        None,
        description="The display name for the task, potentially customized.",
        examples=["Process Customer Data [Region=US]", None]
    )


    class Config:
        json_schema_extra = {
            "example": {
                "dag_id": "data_pipeline",
                "task_id": "extract_data",
                "run_id": "scheduled__2025-04-30T10:00:00+00:00",
                "map_index": -1,
                "start_date": "2025-04-30T10:00:05.123+00:00",
                "end_date": "2025-04-30T10:02:30.456+00:00",
                "duration": 145.333,
                "state": "success",
                "try_number": 1,
                "max_tries": 3,
                "hostname": "worker-1.example.com",
                "unixname": "airflow",
                "job_id": 1234,
                "pool": "default_pool",
                "pool_slots": 1,
                "queue": "default",
                "priority_weight": 1,
                "queued_by_job_id": 56,
                "queued_when": "2025-04-30T10:00:01.000+00:00",
                "pid": 54321,
                "operator": "PythonOperator",
                "executor_config": "{}",
                "updated_at": "2025-04-30T10:02:30.500+00:00",
                "trigger_id": None,
                "trigger_timeout": None,
                "next_method": None,
                "next_kwargs": None,
                "rendered_map_index": -1,
                "task_display_name": "Extract Data"
            }
        }
