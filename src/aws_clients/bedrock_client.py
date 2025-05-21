import boto3

from .sts_client import STSClient

class BedrockClient(STSClient):
    def __init__(self, aws_role_arn, aws_role_session_name):
        super().__init__(aws_role_arn, aws_role_session_name)
        self.set_sts_role_credentials()

    def get_client(self):
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
        )
        return bedrock_client