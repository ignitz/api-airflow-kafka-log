import logging
from typing import Any, Dict, List, Optional
from fastapi import exceptions
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from app.settings.variables import (
    KAFKA_DAG_RUN_TOPIC_NAME,
    KAFKA_TASK_INSTANCE_TOPIC_NAME,
    SCHEMA_REGISTRY_URL,
)
from app.settings.kafka import producer

def delivery_report(err, msg):
    logger = logging.getLogger("publish_message_to_kafka")
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def get_avro_schema(topic) -> str:
    if topic == KAFKA_DAG_RUN_TOPIC_NAME:
        from app.models.dag_run import schema_key, schema_value
        return schema_key, schema_value
    elif topic == KAFKA_TASK_INSTANCE_TOPIC_NAME:
        from app.models.task_instance import schema_key, schema_value
        return schema_key, schema_value
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
        raise exceptions.HTTPException(status_code=500, detail="Failed to flush messages to Kafka")
    logger.info(f"Message published to topic {topic} with key {key} and headers {headers}")

def publish_message_to_kafka_avro(
    topic: str,
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
    schema_key, schema_value = get_avro_schema(topic)
    if not schema_key or not schema_value:
        logger.error(f"Schema not found for topic {topic}")
        raise exceptions.HTTPException(status_code=500, detail="Schema not found for topic")
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    avro_serializer_key = AvroSerializer(schema_registry_client, schema_key)
    avro_serializer_value = AvroSerializer(schema_registry_client, schema_value)
    producer.produce(
        topic=topic,
        value=avro_serializer_value(message, SerializationContext(topic, MessageField.VALUE)),
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
        raise exceptions.HTTPException(status_code=500, detail="Failed to flush messages to Kafka")

def publish_message_to_kafka(
        topic: str,
        message: dict,
        key: Optional[dict] = None,
        headers: Optional[dict] = None,
):
    """
    Publish a message to Kafka.
    """
    if SCHEMA_REGISTRY_URL is not None:
        publish_message_to_kafka_avro(
            topic=topic,
            message=message,
            key=key,
            headers=headers,
        )
    else:
        publish_message_to_kafka_json(
            topic=topic,
            message=message,
            key=key,
            headers=headers,
        )
