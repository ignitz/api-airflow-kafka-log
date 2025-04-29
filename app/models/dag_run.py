schema_key = """
{
    "type": "record",
    "name": "key",
    "fields": [
        {
            "name": "dag_id",
            "type": "string"
        }
    ]
}
"""

schema_value = """
{
  "type": "record",
  "name": "value",
  "doc": "Schema representing the state and details of an Airflow DAG run.",
  "fields": [
    {
      "name": "dag_id",
      "type": "string",
      "doc": "The identifier of the DAG."
    },
    {
      "name": "run_id",
      "type": "string",
      "doc": "The identifier for this specific run of the DAG."
    },
    {
      "name": "run_type",
      "type": "string",
      "doc": "The type classification of the DAG run (e.g., 'manual', 'scheduled')."
    },
    {
      "name": "state",
      "type": ["null", "string"],
      "default": null,
      "doc": "The current state of the DAG run (e.g., 'queued', 'running', 'success', 'failed'). Optional."
    },
    {
      "name": "queued_at",
      "type": ["null", "string"],
      "default": null,
      "doc": "Timestamp (ISO 8601 format preferred) when the run was added to the queue. Optional."
    },
    {
      "name": "execution_date",
      "type": ["null", "string"],
      "default": null,
      "doc": "The logical date/time for which the DAG run is executing (ISO 8601 format preferred). Optional."
    },
    {
      "name": "start_date",
      "type": ["null", "string"],
      "default": null,
      "doc": "Timestamp (ISO 8601 format preferred) when the run actually started execution. Optional."
    },
    {
      "name": "end_date",
      "type": ["null", "string"],
      "default": null,
      "doc": "Timestamp (ISO 8601 format preferred) when the run finished execution. Optional."
    },
    {
      "name": "data_interval_start",
      "type": ["null", "string"],
      "default": null,
      "doc": "Start timestamp (ISO 8601 format preferred) of the data interval covered by this run. Optional."
    },
    {
      "name": "data_interval_end",
      "type": ["null", "string"],
      "default": null,
      "doc": "End timestamp (ISO 8601 format preferred) of the data interval covered by this run. Optional."
    },
    {
      "name": "external_trigger",
      "type": ["null", "boolean"],
      "default": null,
      "doc": "Flag indicating if the run was triggered externally (e.g., via API). Optional."
    },
    {
      "name": "conf",
      "type": ["null", "string"],
      "default": null,
      "doc": "Configuration object passed to the DAG run, typically serialized as a JSON string. Optional."
    },
    {
      "name": "dag_hash_info",
      "type": ["null", "string"],
      "default": null,
      "doc": "Information related to the DAG's version or hash at the time of the run. Optional."
    },
    {
      "name": "msg",
      "type": ["null", "string"],
      "default": null,
      "doc": "An optional descriptive message associated with the event or state change. Optional."
    }
  ]
}
"""