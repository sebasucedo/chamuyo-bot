import boto3

class LambdaClient:
  def __init__(self, name):
    self.name = name
    self.client = boto3.client('lambda')


  def get_arn(self):
    try:
        response = self.client.get_function(FunctionName=self.name)
        return response['Configuration']['FunctionArn']
    except Exception as e:
        print("Error getting function ARN:", str(e))
        return None


  def add_rule_permission(self, rule_arn, hour):
    try:
        response = self.client.add_permission(
            FunctionName=self.name,
            StatementId=f"InvokeFromEventbridge-{self.name}-{hour}",
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_arn
        )
        print("Permission added:", response)
    except Exception as e:
        print("Error adding permission:", str(e))
