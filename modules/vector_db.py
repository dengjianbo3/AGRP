import os
import numpy as np
from pymilvus import MilvusClient, DataType

class MilvusHelper:
    def __init__(self, db_folder='milvus_db'):
        self.db_folder = db_folder
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
    
    def get_milvus_client(self, db_name):
        db_path = os.path.join(self.db_folder, f"{db_name}.db")
        return MilvusClient(db_path)

    def create_collection(self, client, collection_name):
        if not client.has_collection(collection_name):
            client.create_collection(collection_name, dimension=1536)

    def insert_data(self, client, collection_name, texts, embeddings):
        data = [
            {"id": i, "vector": embeddings[i], "text": texts[i], "subject": "history"}
            for i in range(len(embeddings))
        ]
        client.insert(collection_name, data)

    def search(self, client, collection_name, query_vector, top_k):    
        results = client.search(
            collection_name=collection_name,  # target collection
            data=query_vector,  # query vectors
            limit=top_k,  # number of returned entities
            output_fields=["text", "subject"],  # specifies fields to be returned
        )
        return results

