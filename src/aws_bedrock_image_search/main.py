import json
import sys

from aws_clients.bedrock_client import BedrockClient
from config import AppConfig
from helper import get_embedding_from_titan_multimodal, encode_image
from supabase_clients.vecs_client import VecsClient

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from typing import Optional

CONFIG = AppConfig()
DB_CONNECTION = CONFIG.db_connection
AWS_ROLE_ARN = CONFIG.aws_role_arn
AWS_ROLE_SESSION_NAME = CONFIG.aws_role_session_name

def search(query_term: Optional[str] = None):
    if query_term is None:
        query_term = sys.argv[1]

    # Get Bedrock client
    bedrock_client = BedrockClient(AWS_ROLE_ARN,AWS_ROLE_SESSION_NAME).get_client()

    # create vector store client
    vx = VecsClient(DB_CONNECTION).get_client()
    images = vx.get_or_create_collection(name="image_vectors", dimension=1024)

    # Encode text query
    body = json.dumps(
        {
            "inputText": query_term,
            "embeddingConfig": {"outputEmbeddingLength": 1024},
        })

    text_emb = get_embedding_from_titan_multimodal(body,bedrock_client
    )

    # query the collection filtering metadata for "type" = "jpg"
    results = images.query(
        data=text_emb,                      # required
        limit=1,                            # number of records to return
        filters={"type": {"$eq": "jpg"}},   # metadata filters
    )
    result = results[0]
    print(result)
    plt.title(result)
    image = mpimg.imread('./images/' + result)
    plt.imshow(image)
    plt.show()

def seed():

    # Get Bedrock client
    bedrock_client = BedrockClient(AWS_ROLE_ARN,AWS_ROLE_SESSION_NAME).get_client()
    
    # create vector store client
    vx = VecsClient(DB_CONNECTION).get_client()

    # Get or create a collection of vectors with 1024 dimensions
    images = vx.get_or_create_collection(name="image_vectors", dimension=1024)

    # List of image paths
    image_paths = ['./images/one.jpg', './images/two.jpg', './images/three.jpg', './images/four.jpg']

    # Generate image embeddings and construct records for upsert
    records = [
        (img_path.split('/')[-1], encode_image(img_path, bedrock_client), {"type": "jpg"})
        for img_path in image_paths
    ]

    # Add records to the *images* collection
    images.upsert(records=records)
    print("Inserted images")

    # Index the collection for fast search performance
    images.create_index()
    print("Created index")

if __name__ == '__main__':
    search("door")