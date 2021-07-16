# database.py
import pprint

from pymongo import MongoClient
from pymongo import ASCENDING

class MongoDB:
    def __init__(self, db_name='uniswap'):
        self.client = MongoClient()
        self.db = self.client[db_name]

    def get_all_pairs(self):
        pairs = self.db.pairs
        docs = pairs.find()
        return [doc['address'] for doc in docs]

    def get_all_tokens(self):
        tokens = []
        pairs = self.db.pairs
        docs = pairs.find()
        for doc in docs:
            if not doc['token0'] in tokens:
                tokens.append(doc['token0'])
            if not doc['token1'] in tokens:
                tokens.append(doc['token1'])
        return tokens

    def get_token(self, address):
        tokens = self.db.tokens
        tokens.create_index([('address', ASCENDING)], unique=True)
        doc = tokens.find_one({'address': address})
        return doc

    def save_token(self, doc):
        tokens = self.db.tokens
        tokens.create_index([('address', ASCENDING)], unique=True)
        tokens.insert_one(doc)


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