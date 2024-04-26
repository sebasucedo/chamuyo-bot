import boto3
from moto import mock_aws
from utils.EventbridgeClient import EventbridgeClient

class TestEventbridgeClient():
  @mock_aws
  def test_get_rule(self):
    client = boto3.client('events', region_name='us-east-1')

    rule_name = 'chamuyo-bot-rule'
    cron_expression = 'cron(0 12 * * ? *)'
    lambda_arn = 'arn:aws:lambda:us-east-1:123456789012:function:chamuyo-bot'

    client.put_rule(
        Name=rule_name,
        ScheduleExpression=cron_expression
    )

    client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': lambda_arn,
            }
        ]
    )

    eventbridgeClient = EventbridgeClient()

    rule = eventbridgeClient.get_rule(lambda_arn, cron_expression)

    assert rule['Name'] == rule_name
    assert rule['ScheduleExpression'] == cron_expression

