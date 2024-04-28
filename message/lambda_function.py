import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import boto3
from utils.InspirationalMessageGenerator import InspirationalMessageGenerator
from utils.TelegramBot import TelegramBot
from utils.DynamodbClient import DynamodbClient

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChamuyoBot")
dynamodb_client = DynamodbClient(table)
telegramBot = TelegramBot()
generator = InspirationalMessageGenerator()

DEFAULT_EVENT_TIME = "13:00"

def lambda_handler(event, context):
  try:
    eventTime = event.get('detail', {}).get('EventTime')
    print(f"EventTime: {eventTime}")
    if (eventTime is None):
      eventTime = DEFAULT_EVENT_TIME
    
    items = dynamodb_client.get_items_by_event_time(eventTime)
    ids = [item["Id"] for item in items]

    for id in ids:
        print(id)

    message = generator.get_message_content()

    telegramBot.send_messages(ids, message)

  except Exception as e:
    print(f"An error occurred: {e}")
    return {
      'statusCode': 500,
      'body': json.dumps('An error occurred while processing the request.')
    }

  return {
    'statusCode': 200,
    'body': json.dumps('Messages sent!')
  }
