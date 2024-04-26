import boto3
from moto import mock_aws
from utils.LambdaClient import LambdaClient

class TestLambdaClient:
  @mock_aws
  def test_get_arn(self):

    iam = boto3.client('iam', region_name='us-east-1')
    boto3_lambda = boto3.client('lambda', region_name='us-east-1')
    
    assume_role_policy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "lambda.amazonaws.com"},"Action": "sts:AssumeRole"}]}'
    role = iam.create_role(
          RoleName="arn:aws:iam::123456789012:role/test-role",
          AssumeRolePolicyDocument=assume_role_policy
      )
    role_arn = role['Role']['Arn']
  
    response = boto3_lambda.create_function(
      FunctionName="test_function",
      Runtime="python3.8",
      Role=role_arn,
      Handler="lambda_function.lambda_handler",
      Code={"ZipFile": open("webhook/lambda_function.py", "rb").read()}
    )

    lambda_client = LambdaClient("test_function")
    arn = lambda_client.get_arn()

    assert arn == response['FunctionArn']