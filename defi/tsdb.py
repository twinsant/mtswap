#tsdb.py
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "rqi4bsVUxkmdIRxA3vU0-ZzfKG1YuvMk3JCqccC0w942kT8ZSncEMUUbHjoR9NInidBmd6o3ecNIywoxp7vLlQ=="
org = "mytoken"
bucket = "uniswap"


class InfluxDB:
    def __init__(self):
        self.client = InfluxDBClient(url="http://localhost:8086", token=token)

    def save(self, doc):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        point = Point("pair")\
            .tag("address", doc['address'])\
            .field("r0", doc['r0'])\
            .field("r1", doc['r1'])\
            .time(doc['t'], WritePrecision.S)

        write_api.write(bucket, org, point)