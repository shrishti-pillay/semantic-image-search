# AWS Bedrock Image Search

Semantic image search using AWS Bedrock multimodal embeddings and Supabase vector storage.

## Overview

This project demonstrates how to build a semantic image search engine using Amazon Bedrock's Titan multimodal embedding model and Supabase as a vector database. It allows you to encode images and text queries into embeddings, store them, and perform similarity search to find relevant images.

## Features

- Encode images using Amazon Bedrock's Titan multimodal model
- Store and index image embeddings in Supabase (via `vecs`)
- Search images by text queries using semantic similarity
- Simple CLI and scriptable interface

## Project Structure

```
aws_bedrock_image_search/
├── src/
│   ├── aws_bedrock_image_search/
│   │   ├── __init__.py            # Package initializer
│   │   ├── images/                # Directory for storing images to be indexed and searched
│   │   ├── main.py                # Main entry point for seeding and searching
│   │   ├── helper.py              # Helper functions for encoding images and interacting with Bedrock
│   │   └── config.py              # App configuration using Pydantic
│   ├── aws_clients/               # AWS client wrappers for Bedrock and STS
│   │   ├── __init__.py       
│   │   ├── bedrock_client.py      
│   │   └── sts_client.py                  
│   └── supabase_clients/          # Supabase vector client implementation
│       ├── __init__.py           
│       └── vecs_client.py         
├── README.md                      # Project documentation
├── pyproject.toml                 # Poetry configuration and dependencies
├── poetry.lock                    # Poetry lock file
└── .env                           # Environment variables (not committed to version control)

```
## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your system.
- **Poetry** for dependency management (`pip install poetry`).
- **AWS account** with access to Bedrock and permissions to assume roles.
- **Supabase account** for vector database storage.

### Setting up Supabase Database

1. **Create a Supabase Project**
   - Go to [Supabase](https://app.supabase.com/) and sign in.
   - Click "New Project" and follow the prompts to create your project.

2. **Get the Database Connection String**
   - In your Supabase project dashboard, go to `Settings` > `Database`.
   - Copy the `Connection string` (usually starts with `postgres://...`).


3. **Store the Connection String**
   - Add your Supabase connection string to the `.env` file as `db_connection`.

### Setting up AWS IAM Role for Bedrock

1. **Create an IAM Role**
   - Go to the [AWS IAM Console](https://console.aws.amazon.com/iam/).
   - Click "Roles" > "Create role".
   - Create an AWS IAM Role with the following policies:
     - `AmazonBedrockFullAccess` (or a custom policy with Bedrock permissions)
     - Any other policies required for your use case
   - Complete the role creation and note the **Role ARN**.

2. **Store the Role ARN**
   - Add your AWS Role ARN and session name to the `.env` file as `aws_role_arn` and `aws_role_session_name`.

For more information and details on setting up the Supabase Account refer to the blog in the [References](#references) section of this README

You are now ready to use Supabase as your vector database and AWS Bedrock for image embeddings!

## Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd aws_bedrock_image_search
   ```

2. **Create and activate a Python virtual environment**

    ```sh
    python3 -m venv development
    source development/bin/activate
    ```

3. **Install dependencies**

    ```sh
    pip install poetry
    poetry install
    ```

4. **Configure environment variables**

    Create a `.env` file in the project root (src/aws_bedrock_image_search) with the following variables:

    ```
    db_connection=<your_supabase_connection_string>
    aws_role_arn=<your_aws_role_arn>
    aws_role_session_name=<your_session_name>
    ```

5. **Add images**

    Place images you want to index in the `src/aws_bedrock_image_search/images/ `directory (create it if it doesn't exist).

## Usage

### Seed the Database

Generate embeddings for all images and store them in Supabase:

```sh
poetry run seed
```

### Search by Text Query

Search for images similar to a text query:

```sh
cd src/aws_bedrock_image_search/
poetry run search "text" "your search term"
```

### Search by Image Query

Search for images similar to another image:

```sh
cd src/aws_bedrock_image_search/
poetry run search "image" "your/image/path"
```

Or run the script directly:

```sh
cd src/aws_bedrock_image_search/
python3 main.py "text" "your search term"
```

```sh
cd src/aws_bedrock_image_search/
python3 main.py "image" "your/image/path"
```

## Improvements in progress

1. Uploading/downloading images to/from AWS S3 for both seed and search functions.
2. Building Django app for UI interface.


## References
[Semantic Image Search with Amazon Bedrock and Supabase](https://supabase.com/blog/semantic-image-search-amazon-bedrock)