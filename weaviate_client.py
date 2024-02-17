import os
from uuid import uuid4

import weaviate
from requests.exceptions import ConnectionError

class WeaviateClient:
    def __init__(self):
        self.class_name = "DocumentSearch"
        self.client = self.initialize_weaviate_client()

    def initialize_weaviate_client(self):
        try:
            if not os.environ.get("WEAVIATE_URL"):
                print("Unable to connect to Weaviate. Please set the WEAVIATE_URL environment variable.")
                return None

            client = weaviate.Client(url=os.environ.get("WEAVIATE_URL"))
            
            if client.is_ready():
                class_obj = {"class": self.class_name, "vectorizer": "none"}
                client.schema.create_class(class_obj)

            return client
        except weaviate.exceptions.UnexpectedStatusCodeError:
            return client
        except ConnectionError:
            print("Unable to connect to Weaviate. Please check the WEAVIATE_URL environment variable.")
            return None

    def add_vector_to_weaviate(self, text, vector):
        if self.client:
            self.client.data_object.create(
                class_name = self.class_name,
                data_object = {
                    "class_name": self.class_name,
                    "text": text
                },
                vector = vector,
            )
            return True
        return False