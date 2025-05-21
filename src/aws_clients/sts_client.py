import boto3

class STSClient():
    def __init__(self,aws_role_arn,aws_role_session_name):
        #Set STS boto3 client
        self.sts_client = boto3.client("sts")

        # Initialize AWS credentials as None
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_session_token = None

        # Set Role ARN and Role Session Name
        self.aws_role_arn = aws_role_arn
        self.aws_role_session_name = aws_role_session_name
    
    def set_sts_role_credentials(self):
        '''Sets AWS role credentials'''
        try:
            # Call STS API to retreive temporary AWS credentials
            sts_response =  self.sts_client.assume_role(
                RoleArn=self.aws_role_arn,
                RoleSessionName=self.aws_role_session_name
            )
            
            if sts_response: 
                credentials = sts_response.get('Credentials',{})
                self.aws_access_key_id=credentials.get('AccessKeyId')
                self.aws_secret_access_key=credentials.get('SecretAccessKey')
                self.aws_session_token=credentials.get('SessionToken')

        except Exception as e:
            print(f'An error was encountered when trying \
            to assume role {self.aws_role_arn}. Traceback: {str(e)}')

