import json
import asyncio
from ai import get_message_content
from telegram import get_chats, send_messages
from dynamodb import manage_chats


def lambda_handler(event, context):
    try:
        telegra_chats = get_chats()
        chats = manage_chats(telegra_chats['groups'] + telegra_chats['directs'])
        ids = [chat['Id'] for chat in chats]

        message = get_message_content()

        responses = asyncio.run(async_handler(ids, message))
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

async def async_handler(ids, message):
    responses = await send_messages(ids, message)
    await asyncio.sleep(1)
    return responses
    

# lambda_handler(None, None)