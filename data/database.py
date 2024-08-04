from pymongo import MongoClient
from typing import Dict, List

class MongoDBHelper:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_interaction(self, collection_name: str, interaction: Dict):
        collection = self.db[collection_name]
        collection.insert_one(interaction)
    
    def get_interactions(self, collection_name: str, user_id: str) -> List[Dict]:
        collection = self.db[collection_name]
        return list(collection.find({"user_id": user_id}))

    def insert_search_results(self, collection_name: str, search_results: Dict):
        collection = self.db[collection_name]
        collection.insert_one(search_results)

    def get_search_results(self, collection_name: str, user_id: str) -> List[Dict]:
        collection = self.db[collection_name]
        return list(collection.find({"user_id": user_id}))

    def close(self):
        self.client.close()
