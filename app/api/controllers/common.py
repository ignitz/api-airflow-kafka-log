import logging
import json
from typing import Optional, Tuple
from fastapi import exceptions
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from app.settings.variables import (
    KAFKA_AIRFLOW_V2_DAG_RUN_TOPIC_NAME,
    KAFKA_AIRFLOW_V2_TASK_INSTANCE_TOPIC_NAME,
    KAFKA_AIRFLOW_V3_DAG_RUN_TOPIC_NAME,
    KAFKA_AIRFLOW_V3_TASK_INSTANCE_TOPIC_NAME,
    SCHEMA_REGISTRY_URL,
)
from app.settings.kafka import producer


def delivery_report(err, msg):
    logger = logging.getLogger("publish_message_to_kafka")
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def get_avro_schema(topic: str, version: str) -> Tuple[str, str]:
    schema_value = None
    if topic in [KAFKA_AIRFLOW_V2_DAG_RUN_TOPIC_NAME, KAFKA_AIRFLOW_V3_DAG_RUN_TOPIC_NAME]:
        if version == "v3":
            from app.models.airflow_v3.dag_run import DagRun

            schema_value = DagRun.avro_schema()
        elif version == "v2":
            from app.models.airflow_v2.dag_run import DagRun

            schema_value = DagRun.avro_schema()
        else:
            raise ValueError(f"Unknown version: {version}")
        schema_key = {
            "type": "record",
            "name": "key",
            "fields": [
                field for field in schema_value["fields"] if field["name"] == "dag_id"
            ],
        }
        return json.dumps(schema_key), json.dumps(schema_value)
    elif topic in [KAFKA_AIRFLOW_V2_TASK_INSTANCE_TOPIC_NAME, KAFKA_AIRFLOW_V3_TASK_INSTANCE_TOPIC_NAME]:
        if version == "v3":
            from app.models.airflow_v3.task_instance import TaskInstance

            schema_value = TaskInstance.avro_schema()
        elif version == "v2":
            from app.models.airflow_v2.task_instance import TaskInstance

            schema_value = TaskInstance.avro_schema()
        else:
            raise ValueError(f"Unknown version: {version}")
        schema_key = {
            "type": "record",
            "name": "key",
            "fields": [
                field
                for field in schema_value["fields"]
                if field["name"] in ["dag_id", "task_id"]
            ],
        }
        return json.dumps(schema_key), json.dumps(schema_value)
    else:
        raise ValueError(f"Unknown topic: {topic}")


def publish_message_to_kafka_json(
    topic: str,
    message: dict,
    key: Optional[dict] = None,
    headers: dict = None,
):
    """
    Publish a message to Kafka in JSON format.
    """
    import json

    logger = logging.getLogger("publish_message_to_kafka_json")
    if headers is None:
        headers = {}
    producer.produce(
        topic=topic,
        value=json.dumps(message, default=str),
        key=json.dumps(key, default=str) if key else None,
        headers=headers,
        callback=delivery_report,
    )
    if producer.flush(timeout=10) > 0:
        logger.error("Failed to flush messages to Kafka")
        raise exceptions.HTTPException(
            status_code=500, detail="Failed to flush messages to Kafka"
        )
    logger.info(
        f"Message published to topic {topic} with key {key} and headers {headers}"
    )


def publish_message_to_kafka_avro(
    topic: str,
    version: str,
    message: dict,
    key: Optional[dict] = None,
    headers: Optional[dict] = None,
):
    """
    Publish a message to Kafka in Avro format.
    """
    logger = logging.getLogger("publish_message_to_kafka_avro")
    if headers is None:
        headers = {}
    schema_registry_conf = {
        "url": SCHEMA_REGISTRY_URL,
    }
    schema_key, schema_value = get_avro_schema(topic, version)
    if not schema_key or not schema_value:
        logger.error(f"Schema not found for topic {topic}")
        raise exceptions.HTTPException(
            status_code=500, detail="Schema not found for topic"
        )
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    avro_serializer_key = AvroSerializer(schema_registry_client, schema_key)
    avro_serializer_value = AvroSerializer(schema_registry_client, schema_value)
    producer.produce(
        topic=topic,
        value=avro_serializer_value(
            message, SerializationContext(topic, MessageField.VALUE)
        ),
        key=(
            avro_serializer_key(key, SerializationContext(topic, MessageField.KEY))
            if key is not None
            else None
        ),
        headers=headers,
        callback=lambda err, msg: delivery_report(err, msg),
    )
    if producer.flush(timeout=10) > 0:
        logger.error("Failed to flush messages to Kafka")
        raise exceptions.HTTPException(
            status_code=500, detail="Failed to flush messages to Kafka"
        )


def publish_message_to_kafka(
    topic: str,
    version: str,
    message: dict,
    key: Optional[dict] = None,
    headers: Optional[dict] = None,
):
    """
    Publish a message to Kafka.
    """
    if SCHEMA_REGISTRY_URL is not None:
        publish_message_to_kafka_avro(
            topic=topic, message=message, key=key, headers=headers, version=version
        )
    else:
        publish_message_to_kafka_json(
            topic=topic,
            message=message,
            key=key,
            headers=headers,
        )
