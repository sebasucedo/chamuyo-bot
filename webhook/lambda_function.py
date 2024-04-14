import sys
import os
import json
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
        else:
            response_text = f"Unrecognized command: {message_text}"
        send_message(chat_id, response_text)
    else:
        response_text = get_response(message_text)
        send_message(chat_id, response_text)


