import base64
import json
import sys

from matplotlib import pyplot as plt
from matplotlib import image as mpimg

def read_file_as_base64(file_path):
    """Encode image as base64 string."""
    try: 
        with open(file_path, "rb") as image_file: 

            # 1. Read the raw bytes from an image file
            # 2. Encode those bytes into Base64
            # 3. Convert the Base64 bytes into a regular UTF-8 string 
            # (so it's not b'...', but just a string you can print, save, etc.).
            input_image = base64.b64encode(image_file.read()).decode("utf8")
        return input_image
    except: 
        print("bad file name")
        sys.exit(0)

def construct_bedrock_image_body(base64_string):
    """Construct the request body.

    https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-embed-mm.html
    """

    return json.dumps(
        {
            "inputImage": base64_string,
            "embeddingConfig": {"outputEmbeddingLength": 1024}
        }
    )

def get_embedding_from_titan_multimodal(body, bedrock_client):
    '''Invoke the Amazon titan Model via API request.'''

    response = bedrock_client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-image-v1",
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    return response_body["embedding"]

def encode_text(prompt, bedrock_client):
    """Generate embedding from the text prompt."""

    body = json.dumps(
        {
            "inputText": prompt,
            "embeddingConfig": {"outputEmbeddingLength": 1024},
        }
    )
    emb = get_embedding_from_titan_multimodal(body, bedrock_client)
    return emb

def encode_image(file_path, bedrock_client):
    """Generate embedding from the image at file_path."""

    base64_string = read_file_as_base64(file_path)
    body = construct_bedrock_image_body(base64_string)
    emb = get_embedding_from_titan_multimodal(body, bedrock_client)
    return emb

def show_results(results: list):
    result = results[0]
    image = mpimg.imread('./images/' + result)
    plt.imshow(image)
    plt.show()
