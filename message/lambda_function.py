import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from utils.ai import get_message_content
from utils.telegram import get_chats, send_messages
from utils.dynamodb import manage_chats


def lambda_handler(event, context):
    try:
        telegram_chats = get_chats()
        chats = manage_chats(telegram_chats['groups'] + telegram_chats['directs'])
        ids = [chat['Id'] for chat in chats]

        message = get_message_content()

        send_messages(ids, message)

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


# lambda_handler(None, None)