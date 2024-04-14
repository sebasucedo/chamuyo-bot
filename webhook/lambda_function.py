import os
import json
import requests

TOKEN_TELEGRAM = os.getenv('TELEGRAM_TOKEN')

def lambda_handler(event, context):
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]
    incoming_text = message["message"].get("text", "")
    
    handle_command(chat_id, incoming_text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Mensaje procesado correctamente')
    }

def handle_command(chat_id, message_text):
    if message_text.startswith('/'):
        if message_text == '/start':
            response_text = "Hello! I am a bot that will respond to any message you send me."
        else:
            response_text = f"Unrecognized command: {message_text}"
        send_response_to_telegram(chat_id, response_text)
    else:
        response_text = f"Recibí tu mensaje: {message_text}"
        send_response_to_telegram(chat_id, response_text)


def send_response_to_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

