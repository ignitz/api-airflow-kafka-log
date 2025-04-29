import logging
from confluent_kafka import Producer as ConfluentKafkaProducer
from app.settings.variables import KAFKA_BOOTSTRAP_SERVERS, KAFKA_MSK_AWS_REGION
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider


def oauth_cb(oauth_config):
    logger = logging.getLogger("oauth_cb")
    logger.debug(f"oauth_cb: {oauth_config}")
    auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(
        KAFKA_MSK_AWS_REGION, aws_debug_creds=True
    )
    return auth_token, expiry_ms / 1000


def producer_builder():
    logger = logging.getLogger("producer_builder")
    if KAFKA_MSK_AWS_REGION is not None:
        logger.info("Using MSK Kafka with IAM Access Control authentication")
        return ConfluentKafkaProducer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "OAUTHBEARER",
                "oauth_cb": oauth_cb,
            }
        )
    else:  # Local Kafka
        logger.info("Using Local Kafka with no authentication")
        return ConfluentKafkaProducer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "security.protocol": "PLAINTEXT",
            }
        )


producer = producer_builder()
