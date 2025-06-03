import boto3

from botocore.config import Config
from .sts_client import STSClient

class S3Client(STSClient):
    def __init__(self, aws_role_arn, aws_role_session_name):
        super().__init__(aws_role_arn, aws_role_session_name)
        self.set_sts_role_credentials()

    def get_client(self):
        s3_client = boto3.client('s3',  
            region_name='ap-southeast-1', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
        )
        return s3_client
    
    