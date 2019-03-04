#!/usr/bin/python
"""This class consumes data from mentioned Kafka Topic(s)"""

from kafka import KafkaConsumer
from kafka import TopicPartition
from log.log import getLogger
import json
import faust


class MarketConsumer(object):

    logger = getLogger('kafkaconsumer')

    """Instantiating Kafka consumer for given brokers."""
    def __init__(self, kafka_brokers, kafka_topic_name):
        self.logger.info("The kafka broker address:"+kafka_brokers)

        self.kafka_brokers = kafka_brokers
        self.kafka_topic_name = kafka_topic_name

        try:
            self.consumer = KafkaConsumer(bootstrap_servers=kafka_brokers)
        except:
            self.logger.error("Kafka server address is wrong or server is not running")
        try:
            self.partition = TopicPartition(kafka_topic_name, 0)
        except:
            self.logger.error("Check if the topic exists and the partition number is correct")

        self.consumer.assign([self.partition])
    """
    Consuming the input message from the Kafka topic through kafka consumer. Kafka is configured to retain the logs for only 3hours. Consumption from start till end will lead to consumption of transactions in the last 3 hours
    message value and key are raw bytes -- decode if necessary!
    e.g., for unicode: `message.value.decode('utf-8')`
    """
    def consume_all_messages(self):
        self.consumer.seek_to_end()
        end = self.consumer.position(self.partition) - 1
        self.consumer.seek_to_beginning()
        start = self.consumer.position(self.partition) - 1
        list = []
        if start == end:
            self.logger.info("No message in topic")
            self.consumer.close()
            return "No message in topic"
        else:
            for message in self.consumer:
                if message.offset >= end:
                    break
                list.append(json.loads(message.value))
        return list

    async def test_faust(self):
        app = faust.App(
            'nudgeapp',
            broker=self.kafka_brokers,
            value_serializer='raw',
        )

        test_topic = app.topic(self.kafka_topic_name)

        @app.agent(test_topic)
        async def testing_faust_stream(messages):
            async for msg in messages:
                print('Faust messages %s' % msg)

    def consume_some(self, message_count):
        self.consumer.seek_to_beginning()
        start = self.consumer.position(self.partition) - 1
        list = []
        if start:
            for message in self.consumer:
                if message.offset >= message_count:
                    break
                list.append(json.loads(message.value))
        return list
