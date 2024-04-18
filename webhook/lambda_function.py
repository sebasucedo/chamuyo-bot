import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import boto3
from utils.InspirationalMessageGenerator import InspirationalMessageGenerator
from utils.telegram import send_message
from utils.DynamodbClient import DynamodbClient

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChamuyoBot")
dynamodb_client = DynamodbClient(table)

def lambda_handler(event, context):
  try:
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]
    incoming_text = message["message"].get("text", "")  
    
    record_user(chat_id, message)
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
      schedule_event(time_obj)
    else:
      response_text = f"Unrecognized command: {message_text}"
      send_message(chat_id, response_text)
  else:
    generator = InspirationalMessageGenerator()
    response_text = generator.get_response(message_text)
    send_message(chat_id, response_text)


def schedule_event(time_obj):

    #TODO: Implement event scheduling logic here

    time_str = time_obj.strftime('%H:%M')
    print("Scheduling event for: {}".format(time_str))