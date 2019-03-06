#!/usr/bin/python
"""This class produces given input data into mentioned Kafka Topic(s)"""

from kafka import KafkaProducer
import json
from log.log import getLogger

class MarketProducer(object):

    logger = getLogger('kafkaproducer')

    """Instantiating Kafka producer for given brokers."""
    def __init__(self, kafka_brokers):
        self.logger.info("Instantiating Kafka producer for given broker address:"+kafka_brokers)
        try:
            self.producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_brokers
            )
        except Exception as e:
            self.logger.error("Error in Instantiating kafka producer: %s" % e)

    """Streaming the input message to the Kafka topic through kafka producer."""
    def send_transaction_data(self, json_data, kafka_topic_name):
        print("Sending transaction data: %s " % json_data)
        self.producer.send(kafka_topic_name, json_data)
        self.producer.flush()

