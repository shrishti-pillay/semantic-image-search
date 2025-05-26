import os
import sys

from aws_clients.bedrock_client import BedrockClient
from config import AppConfig
from helper import get_embedding_from_titan_multimodal, encode_image, encode_text
from supabase_clients.vecs_client import VecsClient

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from typing import Optional

CONFIG = AppConfig()
DB_CONNECTION = CONFIG.db_connection
AWS_ROLE_ARN = CONFIG.aws_role_arn
AWS_ROLE_SESSION_NAME = CONFIG.aws_role_session_name

def search(query_type: Optional[str] = None, query_term: Optional[str] = None):
    if query_type is None:
        query_type = sys.argv[1] if len(sys.argv) > 2 else None
    if query_term is None:
        query_term = sys.argv[2] if len(sys.argv) > 2 else None

    if query_type and query_term:

        # Get Bedrock client
        bedrock_client = BedrockClient(AWS_ROLE_ARN,AWS_ROLE_SESSION_NAME).get_client()

        # create vector store client
        vx = VecsClient(DB_CONNECTION).get_client()
        images = vx.get_or_create_collection(name="image_vectors", dimension=1024)

        if query_type == 'text':
            emb = encode_text(query_term, bedrock_client)
        elif query_type == 'image':
            emb = encode_image(query_term, bedrock_client)
        else:
            print("Invalid query type. Use 'text' or 'image'.")
            return

        # query the collection filtering metadata for "type" = "jpg"
        results = images.query(
            data=emb,                      # required
            limit=1,                            # number of records to return
            filters={"type": {"$eq": "jpg"}},   # metadata filters
        )
        result = results[0]
        image = mpimg.imread('./images/' + result)
        plt.imshow(image)
        plt.show()
    else:
        print("Please provide the query type and prompt/image path.\nUsage: poetry run search <query_type> <query_term>")

def seed():

    # Get Bedrock client
    bedrock_client = BedrockClient(AWS_ROLE_ARN,AWS_ROLE_SESSION_NAME).get_client()
    
    # create vector store client
    vx = VecsClient(DB_CONNECTION).get_client()

    # Get or create a collection of vectors with 1024 dimensions
    images = vx.get_or_create_collection(name="image_vectors", dimension=1024)

    #Generate image embeddings and construct records for upsert
    records = []
    for img_name in os.listdir('./images'):
        img_path = './images/'+img_name
        records.append((img_name, encode_image(img_path, bedrock_client), {"type": "jpg"}))

    # Add records to the *images* collection
    images.upsert(records=records)
    print("Inserted images")

    # Index the collection for fast search performance
    images.create_index()
    print("Created index")

if __name__ == '__main__':
    search(query_type = sys.argv[1] if len(sys.argv) > 2 else None, 
           query_term=sys.argv[2] if len(sys.argv) > 2 else None)