# database.py
import pprint

from pymongo import MongoClient
from pymongo import ASCENDING

class MongoDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.uniswap

    def get_all_pairs(self):
        pairs = self.db.pairs
        docs = pairs.find()
        return [doc['address'] for doc in docs]

    def getSyncedPairs(self):
        max_idx = 0
        pairs = self.db.pairs
        doc = pairs.find_one(sort=[('idx', -1)])
        if doc:
            max_idx = doc['idx']
        return max_idx

    def save(self, doc):
        pairs = self.db.pairs
        pairs.create_index([('idx', ASCENDING)], unique=True)
        pairs.insert_one(doc)