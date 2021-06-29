import json
from datetime import datetime

from kafka import KafkaProducer
from kafka import KafkaConsumer
from tsdb import InfluxDB


class KafkaDB:
    def __init__(self):
        servers = '127.0.0.1:9092'
        self.producer = KafkaProducer(bootstrap_servers=servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer(bootstrap_servers=servers, value_deserializer=json.loads)
        self.db = InfluxDB()

    def save(self, doc):
        self.producer.send('uniswap', doc)

    def run(self):
        self.consumer.subscribe(['uniswap'])
        for msg in self.consumer:
            doc = msg.value
            doc['t'] = datetime.fromtimestamp(doc['t'])
            self.db.save(doc)

if __name__ == '__main__':
    k = KafkaDB()
    k.run()