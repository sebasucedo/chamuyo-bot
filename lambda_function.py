import json
from ai import get_message_content
from telegram import get_chat_ids, send_messages


def lambda_handler(event, context):
    try:
        chat_ids = get_chat_ids()
        message = get_message_content()
        send_messages(chat_ids, message)
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