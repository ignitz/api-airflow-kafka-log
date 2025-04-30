import datetime
from typing import Dict, Any
from typing import Optional
from pydantic import Field
from app.models.base import AvroBase

class DagRun(AvroBase):
    # --- Core Identifiers ---
    dag_id: str = Field(
        ...,
        description="The unique identifier for the DAG.",
        examples=["my_data_pipeline"]
    )
    run_id: str = Field(
        ...,
        description="The unique identifier for this specific DAG run.",
        examples=["manual__2025-05-01T10:00:00+00:00"]
    )
    # --- Timing & Scheduling ---
    execution_date: datetime.datetime = Field(
        ...,
        description="The logical date for which the DAG run is executing (ISO 8601 format).",
        examples=["2025-05-01T10:00:00+00:00"]
    )
    start_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run actually started execution (ISO 8601 format).",
        examples=["2025-05-01T10:00:05.123+00:00", None]
    )
    end_date: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run finished execution (ISO 8601 format).",
        examples=["2025-05-01T10:30:15.456+00:00", None]
    )
    data_interval_start: Optional[datetime.datetime] = Field(
        None,
        description="The start timestamp of the data interval covered by this DAG run (ISO 8601 format).",
        examples=["2025-05-01T09:00:00+00:00", None]
    )
    data_interval_end: Optional[datetime.datetime] = Field(
        None,
        description="The end timestamp of the data interval covered by this DAG run (ISO 8601 format).",
        examples=["2025-05-01T10:00:00+00:00", None]
    )
    last_scheduling_decision: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp of the last scheduling decision made for this run (ISO 8601 format).",
        examples=["2025-05-01T09:59:58.789+00:00", None]
    )
    queued_at: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when the DAG run was added to the queue (ISO 8601 format).",
        examples=["2025-05-01T09:59:55.123+00:00", None]
    )
    updated_at: Optional[datetime.datetime] = Field(
        None,
        description="Timestamp when this DAG run record was last updated (ISO 8601 format).",
        examples=["2025-05-01T10:30:16.000+00:00", None]
    )

    # # --- State & Type ---
    state: Optional[str] = Field( # Or use DagRunState Enum
        None,
        description="The current state of the DAG run (e.g., 'queued', 'running', 'success', 'failed').",
        examples=["running", "success", None]
    )
    run_type: str = Field( # Or use DagRunType Enum
        ...,
        description="The type of the DAG run (e.g., 'scheduled', 'manual', 'backfill', 'dataset_triggered').",
        examples=["manual", "scheduled"]
    )
    external_trigger: bool = Field(
        ...,
        description="Indicates if the DAG run was triggered externally (e.g., via API, CLI).",
        examples=[True, False]
    )

    # --- Configuration & Context ---
    conf: Optional[str] = Field( # Often stored as JSONB/TEXT in DB
        None,
        description="Configuration parameters passed to the DAG run as a dictionary.",
        examples=["{\"input_path\": \"/data/in\", \"output_path\": \"/data/out\"}", None]
    )
    creating_job_id: Optional[int] = Field(
        None,
        description="The ID of the SchedulerJob or BackfillJob that created this DAG run.",
        examples=[101, None]
    )
    dag_hash: Optional[str] = Field(
        None,
        description="A hash representing the structure of the DAG at the time of the run.",
        examples=["abcdef1234567890", None]
    )
    # Note: Added based on common usage, might need adjustment based on exact version details
    clear_number: Optional[int] = Field(
        None,
        description="A counter incremented when tasks for this run are cleared.",
        examples=[0, 1, None]
    )


    class Config:
        populate_by_name = True
        # Add example for the whole model in generated OpenAPI/JSON Schema docs
        json_schema_extra = {
            "example": {
                "dag_id": "example_etl",
                "run_id": "manual__2025-05-01T11:00:00+00:00",
                "execution_date": "2025-05-01T11:00:00+00:00",
                "start_date": "2025-05-01T11:00:10.000+00:00",
                "end_date": "2025-05-01T11:25:30.000+00:00",
                "data_interval_start": "2025-05-01T10:00:00+00:00",
                "data_interval_end": "2025-05-01T11:00:00+00:00",
                "last_scheduling_decision": "2025-05-01T10:59:55.000+00:00",
                "queued_at": "2025-05-01T10:59:50.000+00:00",
                "updated_at": "2025-05-01T11:25:31.000+00:00",
                "state": "success",
                "run_type": "manual",
                "external_trigger": True,
                "conf": "{\"param1\": \"value1\", \"retries\": 2}",
                "creating_job_id": None,
                "dag_hash": "fedcba9876543210",
                "clear_number": 0
            }
        }