import boto3
import json

lambda_name='chamuyo-bot'

class EventbridgeClient:
  def __init__(self):
    self.client = boto3.client('events')
  

  def get_rule(self, lambda_arn, expected_cron_expression):
    rules_response = self.client.list_rules(
      NamePrefix=lambda_name
    )

    for rule in rules_response['Rules']:
        if rule['ScheduleExpression'] == expected_cron_expression:
            targets_response = self.client.list_targets_by_rule(Rule=rule['Name'])
            for target in targets_response['Targets']:
                if target['Arn'] == lambda_arn:
                    print(f"Regla encontrada: {rule['Name']}")
                    return rule

    return None  


  def schedule_event_if_not_exists(self, lambda_arn, time_obj):
    hour = time_obj.hour
    cron = f"cron(0 {hour} ? * * *)"
    
    rule = self.get_rule(lambda_arn, cron)

    if rule is not None:
      return None
    
    rule_response = self.client.put_rule(
      Name=f"{lambda_name}-{hour}",
      ScheduleExpression=cron,
      State='ENABLED',
      Description=f"Trigger Lambda at {hour}:00"
    )
    rule_name = rule_response['RuleArn'].split('/')[-1]
    rule_arn = rule_response['RuleArn'] 
    
    print(f"rule name: {rule_name}, rule arn: {rule_arn}")

    event_details = {
      "source": "eventtime.source",
      "detail-type": "Scheduled Event",
      "detail": {
        "EventTime": f"{hour}:00"
      }
    }

    target_response = self.client.put_targets(
      Rule=rule_name,
      Targets=[
        {
          'Id': str(hour),
          'Arn': lambda_arn,
          'Input': json.dumps(event_details)
        }
      ]
    )

    if target_response['FailedEntryCount'] > 0:
      print("Error adding targets:", target_response['FailedEntries'])
    else:
      print("Target added successfully")

    return rule_arn
