import datetime
from typing import Optional
from pydantic import Field
from app.models.base import AvroBase

class DagRun(AvroBase):
    """
    Represents a single execution of a Directed Acyclic Graph (DAG) in Apache Airflow.
    """
    dag_id: str = Field(
        ..., # Ellipsis indicates required field
        description="The unique identifier for the DAG.",
        examples=["tutorial", "my_data_pipeline"]
    )
    run_id: str = Field(
        ...,
        description="The unique identifier for this specific DAG run.",
        examples=["manual__2025-04-30T19:08:23.655103+00:00"]
    )
    queued_at: Optional[datetime.datetime] = Field(
        None, # Default value is None, making it optional
        description="Timestamp when the DAG run was added to the queue (ISO 8601 format).",
        examples=["2025-04-30T19:08:23.667685+00:00"]
    )
    start_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run actually started execution (ISO 8601 format).",
        examples=["2025-04-30T19:08:24.067821+00:00"]
    )
    end_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run finished execution (ISO 8601 format).",
        examples=["2025-04-30T19:15:00.123456+00:00", None]
    )
    data_interval_start: Optional[datetime.datetime] = Field(
        None,
        description="The start timestamp of the data interval covered by this DAG run (ISO 8601 format).",
        examples=["2025-04-30T19:00:00+00:00"]
    )
    data_interval_end: Optional[datetime.datetime] = Field(
        None,
        description="The end timestamp of the data interval covered by this DAG run (ISO 8601 format).",
        examples=["2025-04-30T20:00:00+00:00"]
    )
    run_after: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp after which this run is allowed to start (used for scheduling dependencies, ISO 8601 format).",
        examples=["2025-04-30T19:08:22.596000+00:00"]
    )
    last_scheduling_decision: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp of the last scheduling decision made for this run (ISO 8601 format).",
        examples=["2025-04-30T19:08:23.672789+00:00", None]
    )
    updated_at: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run record was last updated (ISO 8601 format).",
        examples=["2025-04-30T19:08:23.672789+00:00"]
    )
    logical_date: datetime.datetime = Field(
        ...,
        description="The logical date/time for which the DAG run is executing (ISO 8601 format). Often synonymous with data_interval_start or execution_date.",
        examples=["2025-04-30T19:08:22.596000+00:00"]
    )
    state: str = Field(
        ...,
        description="The current state of the DAG run (e.g., 'queued', 'running', 'success', 'failed').",
        examples=["running", "success", "failed"]
    )
    run_type: str = Field(
        ...,
        description="The type of the DAG run (e.g., 'scheduled', 'manual', 'backfill', 'dataset_triggered').",
        examples=["manual", "scheduled"]
    )
    triggered_by: str = Field(
        ...,
        description="String representation indicating how the run was triggered (e.g., user, scheduler, API).",
        examples=["DagRunTriggeredByType.REST_API", "DagRunTriggeredByType.SCHEDULER"]
    )
    span_status: str = Field(
        ...,
        description="Status related to OpenTelemetry tracing span, if enabled.",
        examples=["not_started", "running", "completed"]
    )
    creating_job_id: Optional[int] = Field(
        None,
        description="The ID of the SchedulerJob or BackfillJob that created this DAG run.",
        examples=[123, None]
    )
    log_template_id: Optional[int] = Field(
        None,
        description="The ID of the log template used for this run.",
        examples=[1, None]
    )
    scheduled_by_job_id: Optional[int] = Field(
        None,
        description="The ID of the job that scheduled this run (if applicable).",
        examples=[456, None]
    )
    clear_number: int = Field(
        ...,
        description="A counter incremented when tasks for this run are cleared.",
        examples=[0, 1]
    )
    conf: str = Field(
        default_factory="{}",
        description="Configuration parameters passed to the DAG run as a dictionary.",
        examples=['{"key": "value"}', "{}"]
    )
    context_carrier: str = Field(
        default_factory="{}",
        description="Context information for distributed tracing (e.g., OpenTelemetry).",
        examples=['{"traceparent": "00-..."}']
    )
    backfill_id: Optional[str] = Field(
        None,
        description="Identifier if this run is part of a backfill job.",
        examples=["backfill_job_20250430", None]
    )
    bundle_version: Optional[str] = Field(
        None,
        description="Version of the DAG bundle, if applicable (e.g., for DAG versioning).",
        examples=["v1.2.0", None]
    )
    created_dag_version_id: Optional[str] = Field(
        None,
        description="The version ID of the DAG definition used for this run, if versioning is enabled.",
        examples=["01967c74-15ca-76cc-a43b-24335120a6f1", None]
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if the DAG run failed.",
        examples=["Task failed: [task_id]", None]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "dag_id": "tutorial",
                "run_id": "manual__2025-04-30T19:08:23.655103+00:00",
                "queued_at": "2025-04-30T19:08:23.667685+00:00",
                "logical_date": "2025-04-30T19:08:22.596000+00:00",
                "start_date": "2025-04-30T19:08:24.067821+00:00",
                "end_date": None,
                "state": "running",
                "creating_job_id": None,
                "run_type": "manual",
                "triggered_by": "DagRunTriggeredByType.REST_API",
                "conf": {"input_param": "/path/to/data"},
                "data_interval_start": "2025-04-30T19:00:00+00:00",
                "data_interval_end": "2025-04-30T20:00:00+00:00",
                "run_after": "2025-04-30T19:08:22.596000+00:00",
                "last_scheduling_decision": None,
                "log_template_id": 1,
                "updated_at": "2025-04-30T19:08:23.672789+00:00",
                "clear_number": 0,
                "backfill_id": None,
                "bundle_version": None,
                "scheduled_by_job_id": None,
                "context_carrier": {},
                "span_status": "not_started",
                "created_dag_version_id": "01967c74-15ca-76cc-a43b-24335120a6f1",
                "error_message": None,
            }
        }
