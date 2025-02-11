import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3
from utils.InspirationalMessageGenerator import InspirationalMessageGenerator
from utils.TelegramBot import TelegramBot
from utils.DynamodbClient import DynamodbClient
from utils.EventbridgeClient import EventbridgeClient
from utils.LambdaClient import LambdaClient

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChamuyoBot")
dynamodb_client = DynamodbClient(table)
telegramBot = TelegramBot()
eventbridge_client = EventbridgeClient()
lambda_client = LambdaClient("chamuyo-bot")

DEFAULT_EVENT_TIME = "13:00"

def lambda_handler(event, context):
  try:
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]
    incoming_text = message["message"].get("text", "")  
    
    item = dynamodb_client.get_items_by_id(chat_id)
    if item is None:
      record_user(chat_id, message)
      response_text = f"Welcome to ChamuyoBot! I will respond to any message you send me."
      telegramBot.send_message(chat_id, response_text)
    else:
      handle_command(chat_id, incoming_text)
    
    return {
      'statusCode': 200,
      'body': json.dumps("Message processed successfully")
    }
  except Exception as e:
    print(f"An error occurred: {e}")
    return {
      'statusCode': 500,
      'body': json.dumps('An error occurred while processing the request.')
    }


def record_user(chat_id, message):
  try:
    if "message" in message and "from" in message["message"]:
      name = message["message"]["from"].get("username", "")
      type = "direct"
    elif "my_chat_member" in message:
      name = message["my_chat_member"]["chat"].get("title", "")
      type = "group"

    item = {
      "Id": chat_id,
      "EventTime": DEFAULT_EVENT_TIME,
      "Name": name,
      "Type": type
    }

    dynamodb_client.insert(item)
  except Exception as e:
    print(f"An error occurred while inserting chat data: {e}")


def handle_command(chat_id, message_text):
  if message_text.startswith('/'):
    if message_text == '/start':
      response_text = "Hello! I am a bot that will respond to any message you send me."
    if message_text.startswith('/settime '):
      time_string = message_text.split('/settime ')[1].strip()
      time_obj = datetime.strptime(time_string, '%H:%M').time()
      ok = schedule_event(chat_id, time_obj)
      if ok:
        telegramBot.send_message(chat_id, f"Inspirational message scheduled for {time_string}")
    else:
      response_text = f"Unrecognized command: {message_text}"
      telegramBot.send_message(chat_id, response_text)
  else:
    generator = InspirationalMessageGenerator()
    response_text = generator.get_response(message_text)
    telegramBot.send_message(chat_id, response_text)


def schedule_event(chat_id, time_obj):
  try:
    lambda_arn = lambda_client.get_arn()
    print(lambda_arn)

    new_rule_arn = eventbridge_client.schedule_event_if_not_exists(lambda_arn, time_obj)
    if new_rule_arn is not None:
      lambda_client.add_rule_permission(new_rule_arn, time_obj.hour)

    time_str = time_obj.strftime('%H:%M')
    print("Scheduling event for: {}".format(time_str))

    dynamodb_client.update_item(chat_id, "EventTime", time_str)
    return True
  except Exception as e:
    print(f"An error occurred while scheduling event: {e}")
    return False