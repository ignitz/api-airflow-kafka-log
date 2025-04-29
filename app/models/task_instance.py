schema_key = """
{
    "type": "record",
    "name": "key",
    "fields": [
        {
            "name": "dag_id",
            "type": "string"
        },
        {
            "name": "task_id",
            "type": "string"
        }
    ]
}
"""

schema_value = """
{
  "type": "record",
  "name": "value",
  "doc": "Schema representing the state and details of an Airflow Task Instance.",
  "fields": [
    {
      "name": "dag_id",
      "type": "string",
      "doc": "The identifier of the DAG containing the task."
    },
    {
      "name": "task_id",
      "type": "string",
      "doc": "The identifier of the task within the DAG."
    },
    {
      "name": "run_id",
      "type": "string",
      "doc": "The identifier for the specific DAG run associated with this task instance."
    },
    {
      "name": "max_index",
      "type": "int",
      "doc": "The map index for mapped task instances. -1 indicates it's not a mapped task instance."
    },
    {
      "name": "state",
      "type": ["null", "string"],
      "default": null,
      "doc": "The current state of the task instance (e.g., 'queued', 'running', 'success', 'failed', 'skipped'). Optional."
    },
    {
      "name": "start_date",
      "type": ["null", "string"],
      "default": null,
      "doc": "Timestamp (ISO 8601 format preferred) when the task instance started execution. Optional."
    },
    {
      "name": "end_date",
      "type": ["null", "string"],
      "default": null,
      "doc": "Timestamp (ISO 8601 format preferred) when the task instance finished execution. Optional."
    },
    {
      "name": "duration",
      "type": ["null", "float"],
      "default": null,
      "doc": "Duration of the task instance execution in seconds. Optional."
    },
    {
      "name": "try_number",
      "type": ["null", "int"],
      "default": null,
      "doc": "The attempt number for this task instance execution (1-based). Optional."
    },
    {
      "name": "hostname",
      "type": ["null", "string"],
      "default": null,
      "doc": "Hostname of the worker machine that executed the task instance. Optional."
    },
    {
      "name": "unixname",
      "type": ["null", "string"],
      "default": null,
      "doc": "The Unix username under which the task process ran. Optional."
    },
    {
      "name": "job_id",
      "type": ["null", "string"],
      "default": null,
      "doc": "Identifier of the Airflow Job (e.g., LocalTaskJob, CeleryExecutor task ID) that ran the task instance. Optional."
    },
    {
      "name": "pool",
      "type": ["null", "string"],
      "default": null,
      "doc": "The resource pool used by the task instance. Optional."
    },
    {
      "name": "pool_slots",
      "type": ["null", "int"],
      "default": null,
      "doc": "The number of slots in the pool occupied by this task instance. Optional."
    },
    {
      "name": "queue",
      "type": ["null", "string"],
      "default": null,
      "doc": "The queue the task instance was assigned to (relevant for executors like Celery). Optional."
    },
    {
      "name": "priority_weight",
      "type": ["null", "int"],
      "default": null,
      "doc": "The priority weight assigned to the task instance. Optional."
    },
    {
      "name": "operator",
      "type": ["null", "string"],
      "default": null,
      "doc": "The class name of the Airflow operator corresponding to the task. Optional."
    },
    {
      "name": "queued_by_job_id",
       "type": ["null", "string"],
      "default": null,
      "doc": "Identifier of the job that queued the task instance (e.g., SchedulerJob ID). Optional."
    },
    {
      "name": "external_executor_id",
      "type": ["null", "string"],
      "default": null,
      "doc": "An identifier assigned by an external execution system (e.g., Kubernetes pod name). Optional."
    }
  ]
}
"""