import json
from kafka import KafkaProducer
from kafka import KafkaConsumer


class KafkaDB:
    def __init__(self):
        servers = '127.0.0.1:9092'
        self.producer = KafkaProducer(bootstrap_servers=servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer(bootstrap_servers=servers, value_deserializer=json.loads)

    def save(self, doc):
        self.producer.send('uniswap', doc)

    def run(self):
        self.consumer.subscribe(['uniswap'])
        for msg in self.consumer:
            print(msg)

if __name__ == '__main__':
    k = KafkaDB()
    k.run()