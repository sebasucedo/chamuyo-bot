import boto3

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


  def schedule_event(self, time_obj):
    hour = time_obj.hour
    cron = f"cron(0 {hour} ? * * *)"
    
    #TODO: create LambdaClient to get lambda object with name and arn
    lambda_client = boto3.client('lambda')
    lambda_arn = lambda_client.get_function(FunctionName=lambda_name)['Configuration']['FunctionArn']

    print(f"lambda arn:{lambda_arn}")


    rule_name = ""
    rule = self.get_rule(lambda_arn, cron)

    if rule is not None:
      rule_name = rule['Name']
    else:
      rule_response = self.client.put_rule(
        Name=f"{lambda_name}-{hour}",
        ScheduleExpression=cron,
        State='ENABLED',
        Description=f"Trigger Lambda at {hour}:00"
      )
      rule_name = rule_response['RuleArn'].split('/')[-1]
      
    print(f"rule name: {rule_name}")


    target_response = self.client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': str(hour),
                'Arn': lambda_arn
            }
        ]
    )

    if target_response['FailedEntryCount'] > 0:
        print("Error adding targets:", target_response['FailedEntries'])
    else:
        print("Target added successfully")







  # def put_events(self, entries):
  #     return self._eventbridge_client.put_events(Entries=entries)

  # def put_events_with_retry(self, entries, max_retries=3):
  #     for i in range(max_retries):
  #         try:
  #             response = self.put_events(entries)
  #             return response
  #         except Exception as e:
  #             if i == max_retries - 1:
  #                 raise e
  #         time.sleep(2 ** i)