import json
import asyncio
from ai import get_message_content
from telegram import get_chats, send_messages
from dynamodb import manage_chats


async def lambda_handler_async(event, context):
    try:
        telegra_chats = get_chats()
        chats = manage_chats(telegra_chats['groups'] + telegra_chats['directs'])
        ids = [chat['Id'] for chat in chats]

        message = get_message_content()

        responses = await send_messages(ids, message)
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
    return asyncio.run(lambda_handler_async(event, context))


# lambda_handler(None, None)