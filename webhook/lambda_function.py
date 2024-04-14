import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ai import get_response
from utils.telegram import send_message


def lambda_handler(event, context):
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]
    incoming_text = message["message"].get("text", "")
    
    handle_command(chat_id, incoming_text)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Message processed successfully")
    }


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
        response_text = get_response(message_text)
        send_message(chat_id, response_text)


def schedule_event(time_obj):

    #TODO: Implement event scheduling logic here

    time_str = time_obj.strftime('%H:%M')
    print("Scheduling event for: {}".format(time_str))