import json
from kafka import KafkaProducer


class KafkaDB:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def save(self, doc):
        self.producer.send('uniswap', doc)