import json
import asyncio
from ai import get_message_content
from telegram import get_chat_ids, send_messages


async def lambda_handler_async(event, context):
    try:
        chat_ids = get_chat_ids()
        message = get_message_content()

        responses = await send_messages(chat_ids, message)
        for response in responses:
            print(response)
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

def lambda_handler(event, context):
    # github actions test 1
    return asyncio.run(lambda_handler_async(event, context))

# lambda_handler(None, None)